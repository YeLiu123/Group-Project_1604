"""
Full Analysis Pipeline - Team Member 4 (Team Leader)
Integration and execution script that combines all team modules to perform complete quiz analysis

"""

import os
import sys
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Import all team member modules
try:
    from data_extraction_M1 import extract_answers_sequence, write_answers_sequence
    from data_preparation_M2 import download_answer_files, collate_answer_files, simulate_download_from_local
    from data_analysis_M3 import generate_means_sequence, visualize_data, analyze_answer_patterns, generate_means_from_answer_files
    print("✓ Successfully imported all team modules")
except ImportError as e:
    print(f"✗ Error importing modules: {str(e)}")
    print("Please ensure all team member modules are in the same directory")
    sys.exit(1)


class QuizAnalysisPipeline:
    """
    Complete quiz analysis pipeline integrating all team member contributions
    """
    
    def __init__(self, output_dir="analysis_results"):
        """
        Initialize the analysis pipeline
        
        Parameters:
            output_dir (str): Directory for storing analysis results
        """
        self.output_dir = output_dir
        self.data_dir = "data"
        self.collated_file = os.path.join("output", "collated_answers.txt")
        self.results = {}
        self.start_time = time.time()
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"✓ Analysis pipeline initialized - Output directory: {self.output_dir}")
    
    def step1_data_preparation(self, use_local_simulation=True):
        """
        Step 1: Data preparation using Team Member 2's module
        
        Parameters:
            use_local_simulation (bool): Use local files instead of cloud download for testing
        """
        print("\n" + "="*60)
        print("STEP 1: DATA PREPARATION (Team Member 2)")
        print("="*60)
        
        try:
            if use_local_simulation:
                print("Using local file simulation for testing...")
                source_folder = "quiz_answers_named_a1_to_a25"
                if os.path.exists(source_folder):
                    downloaded_count = simulate_download_from_local(source_folder, self.data_dir, 25)
                    self.results['data_preparation'] = {
                        'method': 'local_simulation',
                        'files_processed': downloaded_count,
                        'source_folder': source_folder,
                        'target_folder': self.data_dir
                    }
                    print(f"✓ Successfully simulated download of {downloaded_count} files")
                else:
                    raise FileNotFoundError(f"Source folder not found: {source_folder}")
            else:
                print("Note: For actual cloud download, provide cloud_url parameter")
                print("Using local simulation as fallback...")
                return self.step1_data_preparation(use_local_simulation=True)
            
            # Collate answer files
            print("\nCollating answer files...")
            collated_path = collate_answer_files(self.data_dir)
            self.results['collation'] = {
                'collated_file': collated_path,
                'success': True
            }
            print(f"✓ Files collated successfully: {collated_path}")
            
        except Exception as e:
            print(f"✗ Data preparation failed: {str(e)}")
            self.results['data_preparation'] = {'error': str(e)}
            raise
    
    def step2_answer_extraction(self):
        """
        Step 2: Answer extraction using Team Member 1's module
        """
        print("\n" + "="*60)
        print("STEP 2: ANSWER EXTRACTION (Team Member 1)")
        print("="*60)
        
        try:
            # Find all answer files
            answer_files = []
            for filename in os.listdir(self.data_dir):
                if filename.startswith('answers_respondent_') and filename.endswith('.txt'):
                    answer_files.append(filename)
            
            answer_files.sort(key=lambda x: int(x.replace('answers_respondent_', '').replace('.txt', '')))
            
            if not answer_files:
                raise FileNotFoundError(f"No answer files found in {self.data_dir}")
            
            print(f"Found {len(answer_files)} answer files")
            
            # Extract sequences from each file
            all_sequences = []
            extraction_results = []
            
            for filename in answer_files:
                file_path = os.path.join(self.data_dir, filename)
                try:
                    sequence = extract_answers_sequence(file_path)
                    all_sequences.append(sequence)
                    
                    answered_count = len([a for a in sequence if a > 0])
                    extraction_results.append({
                        'filename': filename,
                        'total_questions': len(sequence),
                        'answered_questions': answered_count,
                        'completion_rate': answered_count / len(sequence) * 100
                    })
                    
                    print(f"✓ {filename}: {answered_count}/100 questions answered ({answered_count}%)")
                    
                    # Also save individual sequence files for further analysis
                    respondent_id = int(filename.replace('answers_respondent_', '').replace('.txt', ''))
                    write_answers_sequence(sequence, respondent_id)
                    
                except Exception as e:
                    print(f"✗ Error processing {filename}: {str(e)}")
                    extraction_results.append({
                        'filename': filename,
                        'error': str(e)
                    })
            
            self.results['answer_extraction'] = {
                'total_files': len(answer_files),
                'successful_extractions': len(all_sequences),
                'all_sequences': all_sequences,
                'extraction_details': extraction_results
            }
            
            print(f"\n✓ Successfully extracted answers from {len(all_sequences)}/{len(answer_files)} files")
            
        except Exception as e:
            print(f"✗ Answer extraction failed: {str(e)}")
            self.results['answer_extraction'] = {'error': str(e)}
            raise
    
    def step3_statistical_analysis(self):
        """
        Step 3: Statistical analysis using Team Member 3's module
        """
        print("\n" + "="*60)
        print("STEP 3: STATISTICAL ANALYSIS (Team Member 3)")
        print("="*60)
        
        try:
            # Method 1: Generate means from collated file
            print("Calculating means from collated answers...")
            if os.path.exists(self.collated_file):
                means_collated = generate_means_sequence(self.collated_file)
                print(f"✓ Means calculated from collated file: {len(means_collated)} questions")
            else:
                means_collated = None
                print("! Collated file not available")
            
            # Method 2: Generate means from answer list files (more reliable)
            print("\nCalculating means from individual answer list files...")
            means_direct = generate_means_from_answer_files()
            
            if means_direct:
                print(f"✓ Means calculated from answer list files: {len(means_direct)} questions")
                
                # Use the more reliable direct method
                means_sequence = means_direct
            elif means_collated:
                print("Using collated file means as fallback")
                means_sequence = means_collated
            else:
                raise ValueError("No valid means could be calculated")
            
            # Calculate comprehensive statistics
            valid_means = [m for m in means_sequence if m > 0]
            
            if not valid_means:
                raise ValueError("No valid answer data found for analysis")
            
            stats = {
                'total_questions': len(means_sequence),
                'answered_questions': len(valid_means),
                'unanswered_questions': len(means_sequence) - len(valid_means),
                'completion_rate': len(valid_means) / len(means_sequence) * 100,
                'overall_mean': np.mean(valid_means),
                'median': np.median(valid_means),
                'std_deviation': np.std(valid_means),
                'min_mean': np.min(valid_means),
                'max_mean': np.max(valid_means),
                'variance': np.var(valid_means)
            }
            
            # Perform pattern analysis
            if os.path.exists(self.collated_file):
                pattern_analysis = analyze_answer_patterns(self.collated_file)
            else:
                pattern_analysis = {"note": "Pattern analysis requires collated file"}
            
            self.results['statistical_analysis'] = {
                'means_sequence': means_sequence,
                'statistics': stats,
                'pattern_analysis': pattern_analysis
            }
            
            print(f"\n✓ Statistical Analysis Results:")
            print(f"   - Questions with responses: {stats['answered_questions']}/100 ({stats['completion_rate']:.1f}%)")
            print(f"   - Overall mean answer: {stats['overall_mean']:.2f}")
            print(f"   - Standard deviation: {stats['std_deviation']:.2f}")
            print(f"   - Answer range: {stats['min_mean']:.2f} - {stats['max_mean']:.2f}")
            
        except Exception as e:
            print(f"✗ Statistical analysis failed: {str(e)}")
            self.results['statistical_analysis'] = {'error': str(e)}
            raise
    
    def step4_pattern_detection(self):
        """
        Step 4: Advanced pattern detection and hypothesis testing
        """
        print("\n" + "="*60)
        print("STEP 4: PATTERN DETECTION & HYPOTHESIS TESTING")
        print("="*60)
        
        try:
            if 'statistical_analysis' not in self.results or 'means_sequence' not in self.results['statistical_analysis']:
                raise ValueError("Statistical analysis must be completed first")
            
            means_sequence = self.results['statistical_analysis']['means_sequence']
            valid_means = [m for m in means_sequence if m > 0]
            
            # Pattern detection algorithms
            patterns_detected = []
            
            # 1. Sequence analysis
            print("Analyzing answer sequences for patterns...")
            
            # Check for arithmetic progressions
            for start in range(len(valid_means) - 2):
                if start + 2 < len(valid_means):
                    diff1 = valid_means[start + 1] - valid_means[start]
                    diff2 = valid_means[start + 2] - valid_means[start + 1]
                    if abs(diff1 - diff2) < 0.1:  # Tolerance for floating point
                        patterns_detected.append({
                            'type': 'arithmetic_progression',
                            'start_position': start,
                            'length': 3,
                            'common_difference': diff1
                        })
            
            # 2. Cyclic pattern detection
            print("Checking for cyclic patterns...")
            for cycle_length in range(2, min(8, len(valid_means) // 2)):
                is_cyclic = True
                for i in range(cycle_length, len(valid_means)):
                    if abs(valid_means[i] - valid_means[i % cycle_length]) > 0.1:
                        is_cyclic = False
                        break
                
                if is_cyclic and cycle_length <= len(valid_means):
                    patterns_detected.append({
                        'type': 'cyclic_pattern',
                        'cycle_length': cycle_length,
                        'pattern': valid_means[:cycle_length]
                    })
                    break
            
            # 3. Statistical randomness test
            print("Testing for randomness vs deliberate patterns...")
            
            # Calculate entropy
            from collections import Counter
            rounded_means = [round(m, 1) for m in valid_means]
            counts = Counter(rounded_means)
            total = len(rounded_means)
            entropy = -sum((count/total) * np.log2(count/total) for count in counts.values() if count > 0)
            
            # Maximum possible entropy for 4 answers
            max_entropy = np.log2(4)
            entropy_ratio = entropy / max_entropy
            
            # Trend analysis
            x = list(range(len(valid_means)))
            correlation = np.corrcoef(x, valid_means)[0, 1] if len(valid_means) > 1 else 0
            
            pattern_tests = {
                'entropy': entropy,
                'entropy_ratio': entropy_ratio,
                'trend_correlation': correlation,
                'randomness_score': entropy_ratio * (1 - abs(correlation))  # Higher = more random
            }
            
            # 4. Answer distribution analysis
            if 'answer_extraction' in self.results and 'all_sequences' in self.results['answer_extraction']:
                all_sequences = self.results['answer_extraction']['all_sequences']
                
                # Count answer distribution across all questions
                answer_counts = {1: 0, 2: 0, 3: 0, 4: 0}
                total_answers = 0
                
                for sequence in all_sequences:
                    for answer in sequence:
                        if answer > 0:
                            answer_counts[answer] += 1
                            total_answers += 1
                
                if total_answers > 0:
                    answer_distribution = {k: v/total_answers for k, v in answer_counts.items()}
                    
                    # Check if distribution is roughly uniform (expected for random)
                    expected_prob = 0.25
                    chi_squared = sum((observed - expected_prob)**2 / expected_prob 
                                    for observed in answer_distribution.values())
                    
                    pattern_tests['answer_distribution'] = answer_distribution
                    pattern_tests['distribution_uniformity'] = chi_squared
            
            self.results['pattern_detection'] = {
                'patterns_found': patterns_detected,
                'pattern_tests': pattern_tests,
                'analysis_summary': self._generate_pattern_summary(patterns_detected, pattern_tests)
            }
            
            print(f"✓ Pattern detection completed:")
            print(f"   - Patterns found: {len(patterns_detected)}")
            print(f"   - Entropy ratio: {pattern_tests['entropy_ratio']:.3f} (1.0 = maximum randomness)")
            print(f"   - Trend correlation: {pattern_tests['trend_correlation']:.3f}")
            print(f"   - Randomness score: {pattern_tests['randomness_score']:.3f}")
            
        except Exception as e:
            print(f"✗ Pattern detection failed: {str(e)}")
            self.results['pattern_detection'] = {'error': str(e)}
            raise
    
    def step5_visualization_and_reporting(self):
        """
        Step 5: Generate visualizations and comprehensive report
        """
        print("\n" + "="*60)
        print("STEP 5: VISUALIZATION & REPORTING")
        print("="*60)
        
        try:
            # Generate visualizations using Team Member 3's module
            if os.path.exists(self.collated_file):
                print("Generating scatter plot visualization...")
                visualize_data(self.collated_file, 1)
                
                print("Generating line plot visualization...")
                visualize_data(self.collated_file, 2)
                
                print("✓ Visualizations generated successfully")
            else:
                print("! Visualizations skipped - collated file not available")
            
            # Generate comprehensive report
            self._generate_comprehensive_report()
            
            print("✓ Analysis report generated")
            
        except Exception as e:
            print(f"✗ Visualization and reporting failed: {str(e)}")
            self.results['visualization'] = {'error': str(e)}
    
    def _generate_pattern_summary(self, patterns, tests):
        """Generate human-readable pattern analysis summary"""
        summary = []
        
        if patterns:
            summary.append(f"PATTERNS DETECTED ({len(patterns)} found):")
            for i, pattern in enumerate(patterns, 1):
                if pattern['type'] == 'arithmetic_progression':
                    summary.append(f"  {i}. Arithmetic progression starting at position {pattern['start_position']}")
                elif pattern['type'] == 'cyclic_pattern':
                    summary.append(f"  {i}. Cyclic pattern with cycle length {pattern['cycle_length']}")
        else:
            summary.append("No clear mathematical patterns detected in answer sequences.")
        
        # Interpret randomness
        randomness = tests.get('randomness_score', 0)
        if randomness > 0.8:
            summary.append("\nRANDOMNESS ANALYSIS: High randomness - answers appear genuinely random")
        elif randomness > 0.5:
            summary.append("\nRANDOMNESS ANALYSIS: Moderate randomness - some structure may be present")
        else:
            summary.append("\nRANDOMNESS ANALYSIS: Low randomness - deliberate pattern likely present")
        
        # Interpret trend
        correlation = tests.get('trend_correlation', 0)
        if abs(correlation) > 0.7:
            trend_direction = "increasing" if correlation > 0 else "decreasing"
            summary.append(f"TREND ANALYSIS: Strong {trend_direction} trend detected (r={correlation:.3f})")
        elif abs(correlation) > 0.3:
            summary.append(f"TREND ANALYSIS: Weak trend present (r={correlation:.3f})")
        else:
            summary.append("TREND ANALYSIS: No significant trend in answer sequence")
        
        return "\n".join(summary)
    
    def _generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        report_path = os.path.join(self.output_dir, "comprehensive_analysis_report.txt")
        
        with open(report_path, 'w', encoding='utf-8') as report:
            report.write("QUIZ ANSWER PATTERN ANALYSIS - COMPREHENSIVE REPORT\n")
            report.write("=" * 80 + "\n")
            report.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Analysis duration: {time.time() - self.start_time:.2f} seconds\n\n")
            
            # Executive Summary
            report.write("EXECUTIVE SUMMARY\n")
            report.write("-" * 40 + "\n")
            
            if 'statistical_analysis' in self.results:
                stats = self.results['statistical_analysis']['statistics']
                report.write(f"Total Questions Analyzed: {stats['total_questions']}\n")
                report.write(f"Questions with Responses: {stats['answered_questions']} ({stats['completion_rate']:.1f}%)\n")
                report.write(f"Overall Mean Answer: {stats['overall_mean']:.2f} (on scale 1-4)\n")
                report.write(f"Standard Deviation: {stats['std_deviation']:.2f}\n\n")
            
            # Pattern Analysis Results
            if 'pattern_detection' in self.results:
                report.write("PATTERN ANALYSIS RESULTS\n")
                report.write("-" * 40 + "\n")
                analysis_summary = self.results['pattern_detection'].get('analysis_summary', 'Analysis incomplete')
                report.write(analysis_summary + "\n\n")
            
            # Detailed Statistics
            report.write("DETAILED STATISTICAL ANALYSIS\n")
            report.write("-" * 40 + "\n")
            if 'statistical_analysis' in self.results:
                stats = self.results['statistical_analysis']['statistics']
                for key, value in stats.items():
                    if isinstance(value, float):
                        report.write(f"{key.replace('_', ' ').title()}: {value:.4f}\n")
                    else:
                        report.write(f"{key.replace('_', ' ').title()}: {value}\n")
                report.write("\n")
            
            # Data Preparation Summary
            if 'data_preparation' in self.results:
                report.write("DATA PREPARATION SUMMARY\n")
                report.write("-" * 40 + "\n")
                prep_data = self.results['data_preparation']
                if 'files_processed' in prep_data:
                    report.write(f"Files processed: {prep_data['files_processed']}\n")
                    report.write(f"Method: {prep_data.get('method', 'Unknown')}\n")
                report.write("\n")
            
            # Answer Extraction Summary
            if 'answer_extraction' in self.results:
                report.write("ANSWER EXTRACTION SUMMARY\n")
                report.write("-" * 40 + "\n")
                extraction_data = self.results['answer_extraction']
                report.write(f"Total files: {extraction_data.get('total_files', 0)}\n")
                report.write(f"Successful extractions: {extraction_data.get('successful_extractions', 0)}\n")
                
                if 'extraction_details' in extraction_data:
                    total_answered = sum(detail.get('answered_questions', 0) 
                                       for detail in extraction_data['extraction_details'] 
                                       if 'answered_questions' in detail)
                    total_possible = extraction_data.get('successful_extractions', 0) * 100
                    if total_possible > 0:
                        overall_completion = total_answered / total_possible * 100
                        report.write(f"Overall completion rate: {overall_completion:.1f}%\n")
                report.write("\n")
            
            # Conclusions
            report.write("CONCLUSIONS AND RECOMMENDATIONS\n")
            report.write("-" * 40 + "\n")
            
            if 'pattern_detection' in self.results:
                patterns = self.results['pattern_detection'].get('patterns_found', [])
                tests = self.results['pattern_detection'].get('pattern_tests', {})
                
                if patterns:
                    report.write("HYPOTHESIS: DELIBERATE PATTERN DETECTED\n")
                    report.write("Evidence suggests the quiz setter may have used a deliberate\n")
                    report.write("pattern in arranging the correct answers.\n\n")
                else:
                    randomness = tests.get('randomness_score', 0.5)
                    if randomness > 0.7:
                        report.write("HYPOTHESIS: RANDOM ANSWER DISTRIBUTION\n")
                        report.write("Evidence suggests answers are randomly distributed\n")
                        report.write("with no deliberate pattern.\n\n")
                    else:
                        report.write("HYPOTHESIS: INCONCLUSIVE\n")
                        report.write("Limited data prevents definitive conclusion about\n")
                        report.write("deliberate vs random answer patterns.\n\n")
            
            report.write("END OF REPORT\n")
            report.write("=" * 80 + "\n")
        
        # Also save results as JSON for programmatic access
        json_path = os.path.join(self.output_dir, "analysis_results.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            # Convert numpy types to native Python types for JSON serialization
            json_results = self._convert_for_json(self.results)
            json.dump(json_results, json_file, indent=2)
        
        print(f"✓ Comprehensive report saved: {report_path}")
        print(f"✓ JSON results saved: {json_path}")
    
    def _convert_for_json(self, obj):
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {key: self._convert_for_json(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_for_json(item) for item in obj]
        elif isinstance(obj, np.float64):
            return float(obj)
        elif isinstance(obj, np.int64):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    def run_complete_analysis(self, cloud_url=None):
        """
        Execute the complete analysis pipeline
        
        Parameters:
            cloud_url (str, optional): URL for cloud file download
        """
        print("QUIZ ANSWER PATTERN ANALYSIS PIPELINE")
        print("Team Integration Project - All Modules")
        print("=" * 80)
        
        try:
            # Execute all pipeline steps
            self.step1_data_preparation(use_local_simulation=(cloud_url is None))
            self.step2_answer_extraction()
            self.step3_statistical_analysis()
            self.step4_pattern_detection()
            self.step5_visualization_and_reporting()
            
            # Final summary
            print("\n" + "="*80)
            print("ANALYSIS PIPELINE COMPLETED SUCCESSFULLY")
            print("="*80)
            
            total_time = time.time() - self.start_time
            print(f"Total execution time: {total_time:.2f} seconds")
            print(f"Results saved to: {self.output_dir}/")
            
            # Display key findings
            if 'pattern_detection' in self.results:
                patterns = self.results['pattern_detection'].get('patterns_found', [])
                print(f"\nKey Findings:")
                print(f"- Patterns detected: {len(patterns)}")
                
                if 'pattern_tests' in self.results['pattern_detection']:
                    tests = self.results['pattern_detection']['pattern_tests']
                    print(f"- Randomness score: {tests.get('randomness_score', 0):.3f}")
                    print(f"- Trend correlation: {tests.get('trend_correlation', 0):.3f}")
            
            return True
            
        except Exception as e:
            print(f"\n✗ PIPELINE FAILED: {str(e)}")
            print(f"Partial results may be available in: {self.output_dir}/")
            return False


def main():
    """
    Main execution function
    """
    print("Starting Quiz Answer Pattern Analysis Pipeline...")
    
    # Initialize pipeline
    pipeline = QuizAnalysisPipeline()
    
    # Run complete analysis
    success = pipeline.run_complete_analysis()
    
    if success:
        print("\n🎉 Analysis completed successfully!")
        print("📊 Check the analysis_results/ directory for detailed findings")
        print("📈 Visualizations should have been displayed during execution")
    else:
        print("\n❌ Analysis failed - see error messages above")
        print("🔧 Check that all module files are present and data is available")
    
    return success


if __name__ == "__main__":
    # Execute the complete analysis pipeline
    main()