'''
Created on Jul 28, 2010

@author: bzfwadem
'''
import libsbml

def handleMathNode(node, argsToReplace=None):
    '''
    Recursive function to evaluate the type of the given libSBML
    ASTNode and build up the FORTRAN math string.
    '''
    if node is None:
        return "None"
    
    # handle node based on node type
    if node.getType() == libsbml.AST_INTEGER:
        return str(node.getInteger())
    elif node.isReal():
        return str(node.getReal())
    elif node.getType() == libsbml.AST_NAME:
        if argsToReplace and node.getName() in argsToReplace.keys():
            return argsToReplace[node.getName()]
        else:
            return node.getName()
    
    elif node.getType() == libsbml.AST_PLUS:
        return "(%s + %s)" % (handleMathNode(node.getLeftChild(), argsToReplace=argsToReplace), handleMathNode(node.getRightChild(), argsToReplace=argsToReplace))
    elif node.getType() == libsbml.AST_MINUS:
        if node.getRightChild():
            return "(%s - %s)" % (handleMathNode(node.getLeftChild(), argsToReplace=argsToReplace), handleMathNode(node.getRightChild(), argsToReplace=argsToReplace))
        else:
            return "(-1.0 * %s)" % handleMathNode(node.getLeftChild(), argsToReplace=argsToReplace)
    elif node.getType() == libsbml.AST_DIVIDE:
        return "(%s / %s)" % (handleMathNode(node.getLeftChild(), argsToReplace=argsToReplace), handleMathNode(node.getRightChild(), argsToReplace=argsToReplace))
    elif node.getType() == libsbml.AST_TIMES:
        return "(%s * %s)" % (handleMathNode(node.getLeftChild(), argsToReplace=argsToReplace), handleMathNode(node.getRightChild(), argsToReplace=argsToReplace))  
    
    elif node.getType() == libsbml.AST_POWER or node.getType() == libsbml.AST_FUNCTION_POWER:
        return "(%s ** %s)" % (handleMathNode(node.getLeftChild(), argsToReplace=argsToReplace), handleMathNode(node.getRightChild(), argsToReplace=argsToReplace))
    elif node.getType() == libsbml.AST_FUNCTION:
        # this has to be handled differently because in this case, we have
        # a function that is defined in the SBML itself
        functionDefinition = self.mainModel.SbmlModel.Item.getFunctionDefinition(node.getName())
        
        numOfArguments = functionDefinition.getNumArguments()
        argsToReplace = {}
        for i in xrange(numOfArguments):
            arg = functionDefinition.getArgument(i)
            key = arg.getName()
            valueNode = node.getChild(i)
            value = handleMathNode(valueNode)
#                if valueNode.isInteger():
#                    value = valueNode.getInteger()
#                elif valueNode.isReal():
#                    value = valueNode.getReal()
#                elif valueNode.isName():
#                    value = valueNode.getName()
#                else:
#                    value = "(non-supported function value)"
            #TODO: elif valueNode.isFunction():
                
            argsToReplace[key] = value
            
        mathNode = functionDefinition.getMath()
        return handleMathNode(mathNode, argsToReplace=argsToReplace)
    elif node.getType() == libsbml.AST_LAMBDA:
        # the right child contains the body of the math expression
        return handleMathNode(node.getRightChild(), argsToReplace=argsToReplace)
    
    
    print node.getType()
    return "unsupported"