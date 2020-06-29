
def isIn(source,target):
    if source is None or target is None:
        return False
    else:
        count = 0
        for index in source:
            if index in target:
                count += 1
                if count <= len(source):
                    return True
                return False