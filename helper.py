
def getManuAndAsin(x):
    if  "ASIN " not in x and "Manufacture " in x:
        manu=x.index('Manufacturer ')
        return ["",x[manu+1].strip()]
    elif "Manufacturer " not in x and "ASIN " in x:
        asin=x.index("ASIN ")
        return [x[asin+1].strip(),""]
    else:
        manu=x.index('Manufacturer ')
        asin=x.index("ASIN ")
        return [x[asin+1].strip(),x[manu+1].strip()]