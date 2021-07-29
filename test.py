# to check arg parser
import argparse

def get_result(oper, op1, op2):
    op1 = float(op1)
    op2 = float(op2)
    if oper=='add':
        return (op1+op2)
    elif oper=="sub":
        return (op1-op2)
    elif oper=="prod":
        return (op1*op2)
    elif oper=="div":
        return (op1/op2)
    else:
        return (999999)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--oper", default="add")
    args.add_argument("--op1", default=2)
    args.add_argument("--op2", default=3)

    parsed_args = args.parse_args()
    print('op1', type(parsed_args.op1))
    op = get_result(parsed_args.oper, parsed_args.op1, parsed_args.op2)
    print('The result of %s operation is %.2f' % (parsed_args.oper, op))
