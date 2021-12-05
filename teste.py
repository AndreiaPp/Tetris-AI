from shape import SHAPES

def main():
    print(type(SHAPES))
    for i in range(len(SHAPES)):
        print(SHAPES[i])
        print(SHAPES[i].name)
        #print(SHAPES[i].dimensions)
        #print(SHAPES[i].plan)
        #print(SHAPES[i].rotation)
        print(SHAPES[i].positions)
        SHAPES[i].set_pos(0,0)
        print(SHAPES[i].positions)
        break

main()
