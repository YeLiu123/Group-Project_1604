"""
Data Analysis Module - Team Member 3
Used for analyzing quiz answer patterns and visualizing data insights

Author: Team Member 3
"""

import os
import re
import tempfile
import matplotlib.pyplot as plt
import numpy as np
from data_extraction_M1 import extract_answers_sequence
from datetime import datetime


def generate_means_sequence(collated_answers_path):
    """
    Generate mean answer values for each question from collated answers file
    
    Parameters:
        collated_answers_path (str): Path to the collated_answers.txt file
        
    Returns:
        list: List of 100 floats representing mean answer value per question 
              (excluding unanswered questions marked as 0)
        
    Raises:
        FileNotFoundError: If collated answers file doesn't exist
        ValueError: If file format is invalid or no valid data found
    """
    # Validate input file exists
    if not os.path.exists(collated_answers_path):
        raise FileNotFoundError(f"Collated answers file not found: {collated_answers_path}")
    
    try:
        # Read the collated file
        with open(collated_answers_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content by asterisk separators to get individual respondents
        # First, find the start of actual respondent data
        start_idx = content.find('RESPONDENT 1')
        if start_idx == -1:
            raise ValueError("Could not find respondent data in collated file")
        
        respondent_content = content[start_idx:]
        # Split only on lines that are exactly a single asterisk
        respondent_sections = re.split(r"(?m)^\*\s*$", respondent_content)
        
        all_answer_sequences = []
        
        print(f"Processing collated answers from: {collated_answers_path}")
        
        for i, section in enumerate(respondent_sections):
            section = section.strip()
            if not section or 'COLLATION COMPLETE' in section or len(section) < 100:
                continue
                
            # Create temporary file for each respondent section
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                    # Extract just the quiz content (skip headers)
                    lines = section.split('\n')
                    quiz_content = []
                    
                    # Find where actual quiz questions start and extract them
                    for line in lines:
                        line = line.strip()
                        if line.startswith('Question ') or line.startswith('['):
                            quiz_content.append(line)
                        elif line.startswith('RESPONDENT ') or line.startswith('----'):
                            continue  # Skip headers
                        elif line == '':
                            quiz_content.append(line)  # Preserve empty lines
                    
                    # Write quiz content to temp file
                    temp_file.write('\n'.join(quiz_content))
                    temp_file_path = temp_file.name
                
                # Extract answers using Team Member 1's function
                answers = extract_answers_sequence(temp_file_path)
                all_answer_sequences.append(answers)
                
                answered_count = len([a for a in answers if a > 0])
                print(f"Processed respondent {len(all_answer_sequences)}: {answered_count} answered questions")
                
                # Clean up temp file
                os.unlink(temp_file_path)
                
            except Exception as e:
                print(f"Warning: Could not process respondent section {i+1}: {str(e)}")
                continue
        
        if not all_answer_sequences:
            raise ValueError("No valid answer sequences found in collated file")
        
        print(f"Successfully processed {len(all_answer_sequences)} respondents")
        
        # Calculate means for each question position
        means_sequence = []
        
        for question_idx in range(100):
            valid_answers = []
            
            # Collect all non-zero answers for this question
            for answers in all_answer_sequences:
                if question_idx < len(answers) and answers[question_idx] > 0:
                    valid_answers.append(answers[question_idx])
            
            # Calculate mean, or 0 if no valid answers
            if valid_answers:
                mean_value = sum(valid_answers) / len(valid_answers)
                means_sequence.append(mean_value)
            else:
                means_sequence.append(0.0)
        
        print(f"Calculated means for {len(means_sequence)} questions")
        print(f"Questions with responses: {len([m for m in means_sequence if m > 0])}")
        
        return means_sequence
        
    except Exception as e:
        raise ValueError(f"Error processing collated answers file: {str(e)}")


def visualize_data(collated_answers_path, n):
    """
    Visualize quiz answer data using different plot types
    
    Parameters:
        collated_answers_path (str): Either path to the data folder (preferred) or
                                     path to the collated_answers.txt file (backward compatible)
        n (int): Plot type selector (1 for scatter plot, 2 for line plot)
        
    Returns:
        None: Displays plot or prints error message
        
    Raises:
        ValueError: If n is not 1 or 2, or if data processing fails
    """
    # Validate plot type parameter
    if n not in [1, 2]:
        error_msg = f"Error: n must be 1 or 2, got {n}"
        print(error_msg)
        return
    
    try:
        print(f"Creating visualization type {n}...")
        # Ensure pics directory exists for saving figures
        pics_dir = "pics"
        os.makedirs(pics_dir, exist_ok=True)
        
        is_dir = os.path.isdir(collated_answers_path)
        is_file = os.path.isfile(collated_answers_path)

        if n == 1:
            # Scatter plot of means sequence
            print("Generating scatter plot of mean answer values...")
            # If a directory is provided, compute means from individual files; else use collated file
            if is_dir:
                # Load sequences from data folder and compute means
                all_sequences = []
                for filename in os.listdir(collated_answers_path):
                    if filename.startswith('answers_respondent_') and filename.endswith('.txt'):
                        file_path = os.path.join(collated_answers_path, filename)
                        try:
                            seq = extract_answers_sequence(file_path)
                            all_sequences.append(seq)
                        except Exception:
                            continue

                if not all_sequences:
                    raise ValueError("No valid answer files found in the provided data folder")

                means_sequence = []
                for question_idx in range(100):
                    vals = [seq[question_idx] for seq in all_sequences if question_idx < len(seq) and seq[question_idx] > 0]
                    means_sequence.append(sum(vals) / len(vals) if vals else 0.0)
            else:
                means_sequence = generate_means_sequence(collated_answers_path)
            
            plt.figure(figsize=(12, 6))
            questions = list(range(1, 101))
            
            # Create scatter plot
            plt.scatter(questions, means_sequence, alpha=0.7, s=30, c='blue', edgecolors='black', linewidth=0.5)
            
            plt.title('Mean Answer Values by Question', fontsize=16, fontweight='bold')
            plt.xlabel('Question Number', fontsize=12)
            plt.ylabel('Mean Answer Value', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xlim(0, 101)
            plt.ylim(0, 4.5)
            
            # Add statistics text
            valid_means = [m for m in means_sequence if m > 0]
            if valid_means:
                overall_mean = sum(valid_means) / len(valid_means)
                plt.axhline(y=overall_mean, color='red', linestyle='--', alpha=0.7, 
                           label=f'Overall Mean: {overall_mean:.2f}')
                plt.legend()
            
            plt.tight_layout()
            # Save then show
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(pics_dir, f"means_scatter_{timestamp}.png")
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
            print(f"Saved scatter plot to: {save_path}")
            plt.show()
            
        elif n == 2:
            # Line plot with all individual answer sequences
            print("Generating line plot of all individual answer sequences...")

            all_sequences = []
            respondent_ids = []

            if is_dir:
                # Load directly from data folder
                files = [f for f in os.listdir(collated_answers_path) if f.startswith('answers_respondent_') and f.endswith('.txt')]
                files.sort(key=lambda x: int(x.replace('answers_respondent_', '').replace('.txt', '')))
                for idx, filename in enumerate(files, start=1):
                    file_path = os.path.join(collated_answers_path, filename)
                    try:
                        seq = extract_answers_sequence(file_path)
                        all_sequences.append(seq)
                        respondent_ids.append(idx)
                    except Exception as e:
                        print(f"Warning: Could not process {filename}: {str(e)}")
                        continue
            elif is_file:
                # Backward compatibility: parse collated file
                with open(collated_answers_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                start_idx = content.find('RESPONDENT 1')
                if start_idx == -1:
                    raise ValueError("Could not find respondent data in collated file")

                respondent_content = content[start_idx:]
                respondent_sections = re.split(r"(?m)^\*\s*$", respondent_content)
                for i, section in enumerate(respondent_sections):
                    section = section.strip()
                    if not section or 'COLLATION COMPLETE' in section or len(section) < 100:
                        continue
                    try:
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                            lines = section.split('\n')
                            quiz_content = []
                            for line in lines:
                                line = line.strip()
                                if line.startswith('Question ') or line.startswith('['):
                                    quiz_content.append(line)
                                elif line.startswith('RESPONDENT ') or line.startswith('----'):
                                    continue
                                elif line == '':
                                    quiz_content.append(line)
                            temp_file.write('\n'.join(quiz_content))
                            temp_file_path = temp_file.name

                        answers = extract_answers_sequence(temp_file_path)
                        all_sequences.append(answers)
                        respondent_ids.append(len(all_sequences))
                        os.unlink(temp_file_path)
                    except Exception as e:
                        print(f"Warning: Could not process respondent {len(all_sequences)+1}: {str(e)}")
                        continue
            else:
                raise ValueError("Provided path is neither a directory nor a file")
            
            if not all_sequences:
                raise ValueError("No valid sequences found for plotting")
            
            # Create line plot
            plt.figure(figsize=(15, 8))
            questions = list(range(1, 101))
            
            # Plot each respondent's sequence
            for i, sequence in enumerate(all_sequences):
                # Keep 0s to visualize unanswered questions at y=0 across 1-100
                plot_sequence = [float(val) for val in sequence]
                plt.plot(questions, plot_sequence, alpha=0.5, linewidth=1, label=f'Respondent {respondent_ids[i]}')
            
            plt.title('Individual Answer Sequences for All Respondents', fontsize=16, fontweight='bold')
            plt.xlabel('Question Number', fontsize=12)
            plt.ylabel('Answer Value', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xlim(1, 100)
            plt.ylim(-0.2, 4.5)
            
            # Set y-axis ticks to include unanswered (0)
            plt.yticks([0, 1, 2, 3, 4], ['Unanswered', 'Answer 1', 'Answer 2', 'Answer 3', 'Answer 4'])
            
            # Baseline for unanswered (y=0)
            plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
            
            # Add legend with limited entries to avoid clutter
            if len(all_sequences) <= 10:
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            else:
                plt.text(0.02, 0.98, f'Showing {len(all_sequences)} respondents', 
                        transform=plt.gca().transAxes, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            # Save then show
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(pics_dir, f"individual_lines_{timestamp}.png")
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
            print(f"Saved line plot to: {save_path}")
            plt.show()
            
        print(f"Visualization type {n} completed successfully!")
        
    except Exception as e:
        error_msg = f"Error creating visualization: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)


def analyze_answer_patterns(collated_answers_path):
    """
    Additional analysis function to identify potential patterns in answers
    
    Parameters:
        collated_answers_path (str): Path to the collated_answers.txt file
        
    Returns:
        dict: Analysis results including statistics and pattern insights
    """
    try:
        means_sequence = generate_means_sequence(collated_answers_path)
        
        # Calculate statistics
        valid_means = [m for m in means_sequence if m > 0]
        
        if not valid_means:
            return {"error": "No valid data for analysis"}
        
        analysis_results = {
            "total_questions": len(means_sequence),
            "answered_questions": len(valid_means),
            "unanswered_questions": len(means_sequence) - len(valid_means),
            "overall_mean": sum(valid_means) / len(valid_means),
            "min_mean": min(valid_means),
            "max_mean": max(valid_means),
            "std_deviation": np.std(valid_means) if len(valid_means) > 1 else 0.0
        }
        
        # Look for potential patterns
        patterns = []
        
        # Check for sequences of similar values
        for i in range(len(valid_means) - 3):
            if abs(valid_means[i] - valid_means[i+1]) < 0.1 and \
               abs(valid_means[i+1] - valid_means[i+2]) < 0.1 and \
               abs(valid_means[i+2] - valid_means[i+3]) < 0.1:
                patterns.append(f"Consistent pattern around questions {i+1}-{i+4}")
        
        analysis_results["patterns"] = patterns
        
        return analysis_results
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


def generate_means_from_answer_files():
    """
    Alternative function to generate means directly from answer list files
    """
    print("Generating means from individual answer list files...")
    
    answer_files = []
    for i in range(1, 26):
        filename = f"answers_list_respondent_{i}.txt"
        if os.path.exists(filename):
            answer_files.append(filename)
    
    if not answer_files:
        print("No answer list files found")
        return None
    
    all_sequences = []
    for filename in answer_files:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            # Find the answer sequence line
            sequence_line = None
            for line in lines:
                if line.startswith("Answer sequence:"):
                    sequence_line = line.strip()
                    break
            
            if sequence_line:
                # Extract numbers from the sequence
                numbers_str = sequence_line.replace("Answer sequence:", "").strip()
                sequence = [int(x) for x in numbers_str.split()]
                all_sequences.append(sequence)
                print(f"Loaded {filename}: {len([x for x in sequence if x > 0])} answered questions")
            
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
    
    if not all_sequences:
        print("No valid sequences found")
        return None
    
    # Calculate means
    means_sequence = []
    for question_idx in range(100):
        valid_answers = []
        for sequence in all_sequences:
            if question_idx < len(sequence) and sequence[question_idx] > 0:
                valid_answers.append(sequence[question_idx])
        
        if valid_answers:
            mean_value = sum(valid_answers) / len(valid_answers)
            means_sequence.append(mean_value)
        else:
            means_sequence.append(0.0)
    
    print(f"Calculated means for {len(means_sequence)} questions from {len(all_sequences)} respondents")
    return means_sequence


if __name__ == "__main__":
    """
    Test module functionality with existing data
    """
    print("Testing Data Analysis Module")
    print("=" * 50)
    
    # Test with answer list files first (more reliable)
    print("\nTest 1a: Generating means from answer list files...")
    try:
        means_direct = generate_means_from_answer_files()
        if means_direct:
            print(f"First 10 means: {[round(m, 2) for m in means_direct[:10]]}")
            valid_means = [m for m in means_direct if m > 0]
            if valid_means:
                print(f"Overall mean: {sum(valid_means)/len(valid_means):.2f}")
                print(f"Questions with responses: {len(valid_means)}/100")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test with existing collated answers file
    collated_file = "output/collated_answers.txt"
    
    if os.path.exists(collated_file):
        print(f"\nTest 1b: Testing with collated file: {collated_file}")
        
        # Test 1: Generate means sequence
        print("\nGenerating means sequence from collated file...")
        try:
            means = generate_means_sequence(collated_file)
            print(f"Successfully generated means for {len(means)} questions")
            print(f"First 10 means: {[round(m, 2) for m in means[:10]]}")
            
            # Show some statistics
            valid_means = [m for m in means if m > 0]
            if valid_means:
                print(f"Overall mean: {sum(valid_means)/len(valid_means):.2f}")
                print(f"Questions with responses: {len(valid_means)}/100")
            
        except Exception as e:
            print(f"Error generating means: {str(e)}")
        
        # Test 2: Pattern analysis
        print("\nTest 2: Analyzing patterns...")
        try:
            analysis = analyze_answer_patterns(collated_file)
            print("Analysis results:")
            for key, value in analysis.items():
                if key != "patterns":
                    print(f"  {key}: {value}")
            
            if "patterns" in analysis and analysis["patterns"]:
                print("  Patterns found:")
                for pattern in analysis["patterns"]:
                    print(f"    - {pattern}")
            
        except Exception as e:
            print(f"Error in pattern analysis: {str(e)}")
        
        # Test 3: Visualizations
        print("\nTest 3: Testing visualization functions...")
        print("Visualization tests:")
        
        # Test invalid n value
        print("- Testing invalid n value...")
        visualize_data(collated_file, 2)  # Should show error
        
        print("- Visualization functions ready (plots can be generated with n=1 or n=2)")
        
    else:
        print(f"Collated answers file not found: {collated_file}")
        print("Please run Team Member 2's module first to generate collated data")
    
    print("\nTesting complete!")