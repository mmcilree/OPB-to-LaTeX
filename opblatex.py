import argparse

def get_latex(opb_path):
    opb_file = open(opb_path)
    opb_lines = opb_file.readlines()
    latex_str = R"\begin{align*}" + "\n"
    for line in opb_lines:
        if line.startswith("*"):
            continue;
        latex_str += "\t"
        terms = line.split(" ")
        
        if terms[0] != "1" and terms[0] != "-1":
            latex_str += terms[0]
        elif terms[0] == "-1":
            latex_str += "-"
        latex_str += get_var_str(terms[1])

        i = 2
        while(terms[i] != ">="):
            latex_str += " + "
            if terms[i] != "1" and terms[i] != "-1":
                latex_str += terms[i] 
            elif terms[i] == "-1":
                latex_str += "-"
            latex_str += get_var_str(terms[i + 1])
            i += 2

        latex_str += R" &\geq "
        latex_str += terms[i + 1].replace("\n", "")

        if i + 2 < len(terms):
            if terms[i + 2] == "<==":
                latex_str += R" \Leftarrow "
                latex_str += get_var_str(terms[i + 3])
            elif terms[i + 2] == "==>":
                latex_str += R" \Rightarrow "
                latex_str += get_var_str(terms[i + 3])
        latex_str += R"; \\" + "\n"
        

    opb_file.close()
    latex_str += R"\end{align*}"
    return latex_str

def get_var_str(var):
    var_split = var.split("_")
    tag = "".join(var_split[1:])
    tag = tag.replace("eq", "=")
    tag = tag.replace("ge", R" \geq ")
    tag = tag.replace("bn", R" \text{neg} ")
    var_split[0] = "x"
    return R"\texttt{" + var_split[0] + "}" + R"_{" + tag + R"}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'OPB to LaTeX',
                    description = 'Convert a pseudo-Boolean .opb file to a LaTeX string')
    
    parser.add_argument("opb_path", help="An opb/veripb file")
    args = parser.parse_args()
    latex_str = get_latex(args.opb_path)
    print(latex_str)