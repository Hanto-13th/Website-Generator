from textnode import TextNode,TextType

def main():
    new_node = TextNode("test123",TextType.IMAGE.value,"abcde.com")
    print(new_node)

main()