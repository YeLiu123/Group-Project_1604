
def extract_answers_sequence(file_path):
    """
    extract the answers from the quiz answers file
    
    parameters:
        file_path (str): the path of the quiz answers file
        
    return:
        list: a list of 100 integers, each integer is 1-4 (corresponding to the selected answer) or 0 (not answered)
        
    exceptions:
        FileNotFoundError: if the specified file does not exist
        ValueError: if the file format is incorrect
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # split the file content into lines
        lines = content.strip().split('\n')
        answers = []
        
        # find the answer of each question
        question_count = 0
        i = 0
        
        while i < len(lines) and question_count < 100:
            line = lines[i].strip()
            
            # check if it is a question line
            if line.startswith(f"Question {question_count + 1}."):
                question_count += 1
                # after finding the question, check the next 4 answer options
                answer_found = 0  # 0 means not answered
                
                # check the next 4 answer options
                for j in range(1, 5):  # check the next 4 lines
                    if i + j < len(lines):
                        answer_line = lines[i + j].strip()
                        if answer_line.startswith('[x]'):
                            answer_found = j  # the jth line corresponds to the jth answer
                            break
                        elif not answer_line.startswith('['):
                            # if it is not an answer line, break the loop
                            break
                
                answers.append(answer_found)
                i += 5  # skip the current question and 4 answer lines
            else:
                i += 1
        
        # ensure there are 100 answers
        while len(answers) < 100:
            answers.append(0)
        
        return answers[:100]  # only return the first 100 answers
        
    except FileNotFoundError:
        raise FileNotFoundError(f"cannot find the file: {file_path}")
    except Exception as e:
        raise ValueError(f"error when parsing the file: {str(e)}")


def write_answers_sequence(answers, n):
    """
    write the answers sequence to a file
    
    parameters:
        answers (list): a list of 100 integers, each integer is 0-4
        n (int): the respondent ID number
        
    return:
        None
        
    exceptions:
        ValueError: if the answers list is not 100 or contains invalid values
        IOError: if an error occurs when writing to the file
    """
    # check the input
    if not isinstance(answers, list):
        raise ValueError("the answers must be a list")
    
    if len(answers) != 100:
        raise ValueError(f"the answers list must contain 100 elements, currently there are {len(answers)} elements")
    
    # check if all answers are integers between 0 and 4
    for i, answer in enumerate(answers):
        if not isinstance(answer, int) or answer < 0 or answer > 4:
            raise ValueError(f"the {i+1}th answer is invalid: {answer}, the answer must be an integer between 0 and 4")
    
    # create the output file name
    output_filename = f"answers_list_respondent_{n}.txt"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            # write the answers sequence to the file, each answer on a new line
            for i, answer in enumerate(answers):
                file.write(f"Question {i+1}: {answer}\n")
            
            # also write a line containing all the answers, for later processing
            file.write("\nAnswer sequence: ")
            file.write(" ".join(map(str, answers)))
            file.write("\n")
        
        print(f"the answers sequence has been successfully written to the file: {output_filename}")
        
    except Exception as e:
        raise IOError(f"error when writing to the file: {str(e)}")


if __name__ == "__main__":
    """
    test code for the module functions
    """
    # test the extraction function
    try:
        print("testing the extraction function...")
        test_file = "quiz_answers_named_a1_to_a25/a1.txt"
        answers = extract_answers_sequence(test_file)
        print(f"successfully extracted {len(answers)} answers")
        print(f"the first 10 answers: {answers[:10]}")
        
        # test the writing function
        print("\ntesting the writing function...")
        write_answers_sequence(answers, 1)
        print("testing completed!")
        
    except Exception as e:
        print(f"error during testing: {str(e)}")