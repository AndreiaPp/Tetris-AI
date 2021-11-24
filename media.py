def media(file):
    soma=0
    counter=0
    while file:
        num = file.readline().strip()
        if num=="":
            break
        soma+=int(num)
        counter+=1
    return soma/counter



def main():
    file = open('scores.txt','r')
    print(media(file))
    file.close()


main()

#Colocar na linha 149 do server
# file = open('scores.txt','a')
#                 file.write(str(self.game.score))
#                 file.write("\n")
#                 file.close()