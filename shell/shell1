#! /usr/bin/env python3

import os, sys, re
loop = True
pip = False
sys.ps1 = os.environ.get('PS1')
if sys.ps1 is None:
    sys.ps1 = '$ '
while loop:
    try:
        reply = input(sys.ps1)
        if reply == "exit":
            loop = False
            continue
        elif reply == "":
            continue
        pid = os.getpid()

        # os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

        for a in reply.split():
            if a == '|':
                args1 = reply.split('|')
                pip = True
                pr, pw = os.pipe()

        rc = os.fork()

        if rc < 0:
            # os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:  # child
            # os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
            if pip:
                os.set_inheritable(pr, True)
                os.set_inheritable(pw, True)
                args = args1[0].split()
                os.close(1)  # redirect child's stdout
                fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                os.dup2(pw, fd)
            else:
                args = reply.split()
                position = 0
                if len(args) > 2:
                    for a in args:
                        if a == '<':
                            os.close(0)  # redirect child's stdin
                            sys.stdin = open(args[position + 1], "r")
                            fd = sys.stdin.fileno()
                            os.set_inheritable(fd, True)
                            args[position] = sys.stdin.read()

                        if a == '>':
                            os.close(1)  # redirect child's stdout
                            sys.stdout = open(args[position + 1], "w")
                            del args[position]
                            args = args[:position]
                            fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                            os.set_inheritable(fd, True)

                            # os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

                        position += 1

            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, args[0])
                # os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
                try:
                    os.execve(program, args, os.environ)  # try to exec program
                except FileNotFoundError:  # ...expected
                    pass  # ...fail quietly

            # os.write(2, "Command not found\n".encode())
            # os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
            sys.exit(1)

        else:  # parent (forked ok)
            if pip:
                os.close(0)  # redirect child's stdin
                fd = sys.stdin.fileno()
                os.dup2(pr, fd)
                args = args1[1].split()

                for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                    program = "%s/%s" % (dir, args[0])
                    # os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
                    try:
                        os.execve(program, args, os.environ)  # try to exec program
                    except FileNotFoundError:  # ...expected
                        pass  # ...fail quietly
                pip = False
            childPidCode = os.wait()

    except EOFError:
            break
    except KeyboardInterrupt:
            break