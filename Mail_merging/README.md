# Mail Merging Project

An automated mail merging system that creates personalized letters from a template.

## Description

This project automates the process of creating personalized letters by replacing placeholders in a template letter with names from a list. It's perfect for sending bulk personalized correspondence.

## Features

- Template-based letter generation
- Automatic name replacement using placeholders
- Bulk letter creation
- Organized file output structure

## Project Structure

```
Input/
├── Letters/
│   └── starting_letter.txt    # Template letter with [name] placeholder
└── Names/
    └── invited_names.txt       # List of recipient names

Output/
└── ReadyToSend/               # Generated personalized letters
```

## How to Use

1. Add recipient names to `Input/Names/invited_names.txt` (one name per line)
2. Create your letter template in `Input/Letters/starting_letter.txt` using `[name]` as placeholder
3. Run main.py
4. Find your personalized letters in the `Output/ReadyToSend/` folder

## Example

If your template contains "Dear [name]," and your names list includes "John", the output will be "Dear John,".

## Dependencies Used

- Python
- File I/O operations
- String manipulation