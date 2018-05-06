import sys

check_indent = True

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

def process(text):
    lines = text.split('\n')
    endif = False
    endfor = False
    conditions = []
    iterations = [None]
    replaces = [None]
    buffers = ['']
    indent = []
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
                code = line[i_code + len(key):]
                i_colon = code.rfind(':')
                if i_colon >= 0: # python code terminates with ':', this is a multi-line
                    code = code[:i_colon]
                else:
                    endif = True
                cond = eval(code)
                conditions.append(cond)
        if i_code < 0:
            key = '*else*'
            i_code = line.find(key)
            if i_code >= 0:
                do_indent(indent, i_code, lines_before, check_indent)
                code = line[i_code + len(key):]
                i_colon = code.rfind(':')
                if i_colon >= 0: # python code terminates with ':', this is a multi-line
                    code = code[:i_colon]
                else:
                    endif = True
                conditions.append(not last_cond)
        if i_code < 0:
            key = '*elif*'
            i_code = line.find(key)
            if i_code >= 0:
                do_indent(indent, i_code, lines_before, check_indent)
                code = line[i_code + len(key):]
                i_colon = code.rfind(':')
                if i_colon >= 0: # python code terminates with ':', this is a multi-line
                    code = code[:i_colon]
                else:
                    endif = True
                cond = eval(code)
                conditions.append(cond and not last_cond)
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
                code = line[i_code + len(key):]
                i_colon = code.rfind(':')
                if i_colon >= 0: # python code terminates with ':', this is a multi-line
                    code = code[:i_colon]
                else:
                    endfor = True
                key_in = ' in '
                i_in = code.find(key_in)
                keys_to_replace = code[:i_in].strip().split(',')
                for i in range(len(keys_to_replace)):
                    keys_to_replace[i] = keys_to_replace[i].strip()
                replaces.append(keys_to_replace)
                it = eval(code[i_in + len(key_in):])
                iterations.append(it)
                buffers.append('')
        if i_code < 0:
            key = '*endfor*'
            i_code = line.find(key)
            if i_code >= 0:
                endfor = True

        # process conditions and iterations
        cond = True
        for i in conditions:
            cond = cond and i
        if cond:
            if i_code >= 0: # remove python code if there is some
                line_without_code = line[:i_code].rstrip()
            else:
                line_without_code = line
            buffers[-1] += line_without_code + '\n'
            if endfor:
                for it in iterations[-1]:
                    buffer = buffers[-1]
                    if len(replaces[-1]) == 1:  # iterations[-1] is a list
                        it2 = [it]
                    else:                       # iterations[-1] is a list of lists
                        it2 = it
                    for i in range(len(replaces[-1])):
                        buffer = buffer.replace(replaces[-1][i], str(it2[i]))
                    buffers[-2] += buffer

        # close *if* and *for* blocks
        if endif:
            undo_indent(indent, i_code, lines_before, check_indent)
            endif = False
            last_cond = conditions.pop()
        if endfor:
            undo_indent(indent, i_code, lines_before, check_indent)
            endfor = False
            iterations.pop()
            buffers.pop()
            replaces.pop()
    return buffers[0]
