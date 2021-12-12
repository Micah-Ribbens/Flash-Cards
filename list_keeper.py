class ListKeeper:
    def list_to_string(list):
        string = "["
        max_index = len(list)
        for x in range(max_index):
            # Turns the item into a string
            item = str(list[x])

            if x != max_index - 1:
                string += item + ", "

            else:
                string += item + "]"
            
        return string

    def save(list):
        writable_file = open("cards.txt", "w")
        writable_file.write(ListKeeper.list_to_string(list))
        writable_file.close()
    
    def get():
        readable_file = open("cards.txt", "r")
        string = readable_file.read()
        readable_file.close()
        return ListKeeper.string_to_list(string)


    def string_to_list(string):
        skip_next_ch = False
        word = ""
        list = []
        for ch in string:
            if skip_next_ch:
                skip_next_ch = False
                continue

            if ch == "[":
                continue
            
            if ch == ",":
                skip_next_ch = True
                list.append(word)
                word = ""
                continue
            
            word += ch

            if ch == "]":
                break

        list.append(word)
        return list
