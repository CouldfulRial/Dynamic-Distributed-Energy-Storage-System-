while(1):
    text = input("input the coordinates: ")
    coords = text.split(",")

    print("\t[", end="")
    i = 0
    for coord in coords:
        idx = i % 2
        if idx == 0:
            print("(", end="")

        print(coord, end="")
        if idx == 0:
            print(", ", end="")

        if idx == 1:
            print(")", end="")

            if coord != coords[-1]:
                print(", ", end="")

        i += 1

    print("], \n")

