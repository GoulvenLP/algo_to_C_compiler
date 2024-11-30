
class AstNode:

    def accept(self, visitor):
        className = self.__class__.__name__
        method_name = "visit" + self.__class__.__name__
        visit_method = getattr(visitor, method_name, None)
        if visit_method: #errors control
            visit_method(self)
        else:
            raise AttributeError(f"No visit method found for {method_name}")
