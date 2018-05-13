import sys

check_indent = True
new_text = []

def process(text):
    '''
    This is where the templating occurs.
    '''
    global new_text
    lines = text.splitlines()
    endif = False
    endfor = False
    indent = []
    indentation = ''
    spaces = '    '
    replaces = [[]]
    pycode = 'text = []\n\n'
    lines_before = []
    for line in lines:
        lines_before.append(line)
        if len(lines_before) > 20:
            lines_before = lines_before[1:]
        # parse code
        i_code = -1
        if i_code < 0:
            key = '*if*'
            i_code = line.find(key)
            if i_code >= 0:
                do_indent(indent, i_code, lines_before, check_indent)
                code = line[i_code + len(key):].rstrip()
                if code.endswith(':'): # python code terminates with ':', this is a multi-line
                    pass
                else:
                    code += ':'
                    endif = True
                pycode += indentation + 'if' + code + '\n'
                indentation += spaces
        if i_code < 0:
            key = '*else*'
            i_code = line.find(key)
            if i_code >= 0:
                do_indent(indent, i_code, lines_before, check_indent)
                code = line[i_code + len(key):].rstrip()
                if code.endswith(':'): # python code terminates with ':', this is a multi-line
                    pass
                else:
                    code += ':'
                    endif = True
                pycode += indentation + 'else' + code + '\n'
                indentation += spaces
        if i_code < 0:
            key = '*elif*'
            i_code = line.find(key)
            if i_code >= 0:
                do_indent(indent, i_code, lines_before, check_indent)
                code = line[i_code + len(key):].rstrip()
                if code.endswith(':'): # python code terminates with ':', this is a multi-line
                    pass
                else:
                    code += ':'
                    endif = True
                pycode += indentation + 'elif' + code + '\n'
                indentation += spaces
        if i_code < 0:
            key = '*endif*'
            i_code = line.find(key)
            if i_code >= 0:
                endif = True
        if i_code < 0:
            key = '*for*'
            i_code = line.find(key)
            if i_code >= 0:
                do_indent(indent, i_code, lines_before, check_indent)
                code = line[i_code + len(key):].rstrip()
                if code.endswith(':'): # python code terminates with ':', this is a multi-line
                    pass
                else:
                    code += ':'
                    endfor = True
                key_in = ' in '
                i_in = code.find(key_in)
                tokens_to_replace = code[:i_in].strip().split(',')
                for i in range(len(tokens_to_replace)):
                    tokens_to_replace[i] = tokens_to_replace[i].strip()
                replaces.append(tokens_to_replace)
                pycode += indentation + 'for' + code + '\n'
                indentation += spaces
        if i_code < 0:
            key = '*endfor*'
            i_code = line.find(key)
            if i_code >= 0:
                endfor = True

        skip_line = False
        if i_code >= 0: # remove python code if there is some
            line_without_code = line[:i_code].rstrip()
            if line_without_code == '':
                skip_line = True
        else:
            line_without_code = line

        if not skip_line:
            pycode += indentation + 'line = "' + line_without_code + '"\n'
            if len(replaces[-1]) > 0:
                for token in replaces[-1]:
                    pycode += indentation + 'line = line.replace("' + token + '", str(' + token + '))\n'
            pycode += indentation + 'text.append(line)\n'

        # close *if* and *for* blocks
        if endif:
            undo_indent(indent, i_code, lines_before, check_indent)
            indentation = indentation[:-len(spaces)]
            endif = False
        if endfor:
            undo_indent(indent, i_code, lines_before, check_indent)
            indentation = indentation[:-len(spaces)]
            replaces.pop()
            endfor = False
    pycode += 'new_text.append(text)\n'
    exec(pycode)
    return '\n'.join(new_text[-1])

def indent(text, column=1, spaces=4):
    '''
    Indent the right-side code from the given column number (or further if it would overwrite the original text).
    '''
    indentations = [column]
    lines = text.splitlines()
    # first pass is to compute the column numbers and adjust with the longest text line
    for line in lines:
        tokens = ('*if*', '*elif*', '*else*', '*for*')
        for token in tokens:
            if token in line:
                i_code = line.find(token)
                line_length = len(line[:i_code].rstrip())
                if line_length >= indentations[-1]:
                    more_spaces = line_length - indentations[-1] + 1 + spaces
                    indentations = [i + more_spaces for i in indentations]
                code = line[i_code:].rstrip()
                if code.endswith(':'):
                    indentations.append(indentations[-1] + spaces)
                else:
                    indentations.append(indentations[-1])
                break
        endtokens = ('*endif*', '*endfor*')
        for endtoken in endtokens:
            if endtoken in line:
                i_code = line.find(endtoken)
                line_length = len(line[:i_code].rstrip())
                indentations[-1] = indentations[-1] - spaces
                if line_length >= indentations[-1]:
                    more_spaces = line_length - indentations[-1] + 1 + spaces
                    indentations = [i + more_spaces for i in indentations]
                indentations.append(indentations[-1])
                break
    i_ind = 0
    for i_line, line in enumerate(lines):
        tokens = ('*if*', '*elif*', '*else*', '*for*', '*endif*', '*endfor*')
        for token in tokens:
            if token in line:
                i_code = line.find(token)
                new_line = line[:i_code].rstrip()
                new_line += (indentations[i_ind] - len(new_line) - 1) * ' ' + line[i_code:].rstrip()
                lines[i_line] = new_line
                i_ind += 1
                break
    return '\n'.join(lines)

def do_indent(indent, i_code, lines_before, check_indent=True):
    if check_indent:
        if len(indent) != 0:
            if i_code <= indent[-1]:
                print("Indentation error at last line (column should be > " + str(indent[-1] + 1) + ", but it's " + str(i_code + 1) + "):")
                for line in lines_before:
                    print(line)
                sys.exit()
        indent.append(i_code)

def undo_indent(indent, i_code, lines_before, check_indent=True):
    if check_indent:
        if indent[-1] != i_code:
            print("Indentation error at last line (column should be " + str(indent[-1] + 1) + ", but it's " + str(i_code + 1) + "):")
            for line in lines_before:
                print(line)
            sys.exit()
        else:
            indent.pop()
