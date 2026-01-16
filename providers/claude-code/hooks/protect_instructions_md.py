#!/usr/bin/env python3
"""
Hook to prevent modifications to instruction files (AGENTS.md or CLAUDE.md).
Protects both user-level and project-level instruction files from being edited.
"""
import json
import sys
import os

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        
        # Check only file modification tools
        if tool_name not in ['Edit', 'MultiEdit', 'Write', 'NotebookEdit']:
            sys.exit(0)
            
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        # Check if the file being modified is an instruction file
        protected_names = {'AGENTS.MD', 'CLAUDE.MD'}
        if os.path.basename(file_path).upper() in protected_names:
            print("BLOCKED: Cannot modify instruction files (AGENTS.md, CLAUDE.md)")
            print("\nInstruction files contain user guidance and should be modified manually.")
            print("These files are protected from automated modifications.")

            # Provide context about which instructions file was attempted
            if '.claude' in file_path:
                if os.path.expanduser('~') in file_path:
                    print("\nAttempted to modify: User-level instructions file (~/.claude)")
                else:
                    print("\nAttempted to modify: Project-level instructions file (.claude)")

            print("\nIf you need to update instructions, edit the file manually.")
            
            sys.exit(2)  # Exit code 2 blocks the command
            
    except Exception as e:
        # Silent fail - don't break the assistant workflow
        sys.exit(0)

if __name__ == '__main__':
    main()
