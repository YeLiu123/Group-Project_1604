"""
Data Preparation Module - Team Member 2
Used for downloading quiz answer files from cloud services and collating them into unified format

Author: Team Member 2
Date: 2024
"""

import os
import requests
from pathlib import Path
import shutil


def download_answer_files(cloud_url, path_to_data_folder, respondent_index):
    """
    Download answer files from cloud service and rename them appropriately
    
    Parameters:
        cloud_url (str): Base URL of cloud service containing files a1.txt, a2.txt, etc.
        path_to_data_folder (str): Path to the data folder where files should be saved
        respondent_index (int): Number of respondents/files to download (downloads a1.txt to an.txt)
        
    Returns:
        int: Number of files successfully downloaded
        
    Raises:
        ValueError: If respondent_index is not positive
        requests.RequestException: If network/download errors occur
        OSError: If file system operations fail
    """
    # Validate input parameters
    if not isinstance(respondent_index, int) or respondent_index <= 0:
        raise ValueError(f"respondent_index must be a positive integer, got: {respondent_index}")
    
    if not cloud_url:
        raise ValueError("cloud_url cannot be empty")
    
    # Ensure cloud_url ends with '/' for proper URL construction
    if not cloud_url.endswith('/'):
        cloud_url += '/'
    
    # Create data folder if it doesn't exist
    try:
        Path(path_to_data_folder).mkdir(parents=True, exist_ok=True)
        print(f"Created/verified data folder: {path_to_data_folder}")
    except OSError as e:
        raise OSError(f"Failed to create data folder {path_to_data_folder}: {str(e)}")
    
    successful_downloads = 0
    failed_downloads = []
    
    # Download files from a1.txt to an.txt
    for i in range(1, respondent_index + 1):
        source_filename = f"a{i}.txt"
        target_filename = f"answers_respondent_{i}.txt"
        
        # Construct full URLs and paths
        source_url = cloud_url + source_filename
        target_path = os.path.join(path_to_data_folder, target_filename)
        
        try:
            print(f"Downloading {source_filename} from {source_url}...")
            
            # Download file with timeout and proper headers
            response = requests.get(source_url, timeout=30)
            response.raise_for_status()  # Raises HTTPError for bad responses
            
            # Save file with new name
            with open(target_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            
            print(f"Successfully saved as {target_filename}")
            successful_downloads += 1
            
        except requests.exceptions.Timeout:
            error_msg = f"Timeout downloading {source_filename}"
            print(f"Error: {error_msg}")
            failed_downloads.append((source_filename, error_msg))
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error downloading {source_filename}: {e.response.status_code}"
            print(f"Error: {error_msg}")
            failed_downloads.append((source_filename, error_msg))
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error downloading {source_filename}: {str(e)}"
            print(f"Error: {error_msg}")
            failed_downloads.append((source_filename, error_msg))
            
        except OSError as e:
            error_msg = f"File system error saving {target_filename}: {str(e)}"
            print(f"Error: {error_msg}")
            failed_downloads.append((source_filename, error_msg))
    
    # Summary report
    print(f"\nDownload Summary:")
    print(f"Successfully downloaded: {successful_downloads}/{respondent_index} files")
    
    if failed_downloads:
        print(f"Failed downloads: {len(failed_downloads)}")
        for filename, error in failed_downloads:
            print(f"  - {filename}: {error}")
    
    return successful_downloads


def collate_answer_files(data_folder_path):
    """
    Collate all individual answer files into a single unified file
    
    Parameters:
        data_folder_path (str): Path to folder containing individual answer files
        
    Returns:
        str: Path to the created collated_answers.txt file
        
    Raises:
        FileNotFoundError: If data folder doesn't exist or no answer files found
        OSError: If file operations fail
    """
    # Validate data folder exists
    if not os.path.exists(data_folder_path):
        raise FileNotFoundError(f"Data folder not found: {data_folder_path}")
    
    if not os.path.isdir(data_folder_path):
        raise ValueError(f"Path is not a directory: {data_folder_path}")
    
    # Find all answer files (both formats)
    answer_files = []
    
    # Look for both possible naming patterns
    for filename in os.listdir(data_folder_path):
        if (filename.startswith('answers_respondent_') and filename.endswith('.txt')) or \
           (filename.startswith('answers_list_respondent_') and filename.endswith('.txt')):
            answer_files.append(filename)
    
    if not answer_files:
        raise FileNotFoundError(f"No answer files found in {data_folder_path}")
    
    # Sort files by respondent number for consistent ordering
    def extract_respondent_number(filename):
        try:
            # Extract number from both naming patterns
            if filename.startswith('answers_respondent_'):
                return int(filename.replace('answers_respondent_', '').replace('.txt', ''))
            elif filename.startswith('answers_list_respondent_'):
                return int(filename.replace('answers_list_respondent_', '').replace('.txt', ''))
            return 0
        except ValueError:
            return 0
    
    answer_files.sort(key=extract_respondent_number)
    
    # Create output directory
    output_dir = "output"
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        print(f"Created/verified output folder: {output_dir}")
    except OSError as e:
        raise OSError(f"Failed to create output folder {output_dir}: {str(e)}")
    
    # Create collated file
    collated_file_path = os.path.join(output_dir, "collated_answers.txt")
    
    try:
        with open(collated_file_path, 'w', encoding='utf-8') as collated_file:
            collated_file.write("COLLATED QUIZ ANSWERS\n")
            collated_file.write("=" * 50 + "\n\n")
            
            for i, filename in enumerate(answer_files):
                file_path = os.path.join(data_folder_path, filename)
                
                print(f"Processing {filename}...")
                
                # Write respondent header
                respondent_num = extract_respondent_number(filename)
                collated_file.write(f"RESPONDENT {respondent_num}\n")
                collated_file.write("-" * 20 + "\n")
                
                # Read and write file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as individual_file:
                        content = individual_file.read().strip()
                        collated_file.write(content)
                        collated_file.write("\n\n")
                        
                except Exception as e:
                    error_msg = f"Error reading {filename}: {str(e)}"
                    print(f"Warning: {error_msg}")
                    collated_file.write(f"ERROR: {error_msg}\n\n")
                
                # Add separator between respondents (except for the last one)
                if i < len(answer_files) - 1:
                    collated_file.write("*\n\n")
            
            # Add final summary
            collated_file.write("=" * 50 + "\n")
            collated_file.write(f"COLLATION COMPLETE - {len(answer_files)} FILES PROCESSED\n")
    
        print(f"\nCollation completed successfully!")
        print(f"Processed {len(answer_files)} answer files")
        print(f"Output saved to: {collated_file_path}")
        
        return collated_file_path
        
    except OSError as e:
        raise OSError(f"Failed to create collated file: {str(e)}")


def simulate_download_from_local(source_folder, target_folder, respondent_count):
    """
    Simulate cloud download by copying local files (for testing purposes)
    
    Parameters:
        source_folder (str): Folder containing a1.txt, a2.txt, etc.
        target_folder (str): Target data folder
        respondent_count (int): Number of files to copy
        
    Returns:
        int: Number of files successfully copied
    """
    print("SIMULATION MODE: Copying local files instead of downloading")
    
    # Create target folder
    Path(target_folder).mkdir(parents=True, exist_ok=True)
    
    successful_copies = 0
    
    for i in range(1, respondent_count + 1):
        source_file = os.path.join(source_folder, f"a{i}.txt")
        target_file = os.path.join(target_folder, f"answers_respondent_{i}.txt")
        
        try:
            if os.path.exists(source_file):
                shutil.copy2(source_file, target_file)
                print(f"Copied a{i}.txt -> answers_respondent_{i}.txt")
                successful_copies += 1
            else:
                print(f"Warning: Source file {source_file} not found")
                
        except Exception as e:
            print(f"Error copying a{i}.txt: {str(e)}")
    
    print(f"Simulation complete: {successful_copies}/{respondent_count} files copied")
    return successful_copies


if __name__ == "__main__":
    """
    Test module functionality with sample data
    """
    print("Testing Data Preparation Module")
    print("=" * 50)
    
    # Test 1: Simulate download (using local files for testing)
    print("\nTest 1: Simulating file download...")
    try:
        source_folder = "quiz_answers_named_a1_to_a25"
        target_folder = "data"
        
        if os.path.exists(source_folder):
            copied_count = simulate_download_from_local(source_folder, target_folder, 25)
            print(f"Successfully simulated download of {copied_count} files")
        else:
            print("Source folder not found - skipping download simulation")
    
    except Exception as e:
        print(f"Download simulation failed: {str(e)}")
    
    # Test 2: Collate answer files
    print("\nTest 2: Collating answer files...")
    try:
        # First try with the data folder if it exists
        if os.path.exists("data"):
            collated_path = collate_answer_files("data")
        else:
            # Fallback to current directory with existing answer list files
            collated_path = collate_answer_files(".")
        
        print(f"Collation successful: {collated_path}")
        
    except Exception as e:
        print(f"Collation failed: {str(e)}")
    
    print("\nTesting complete!")