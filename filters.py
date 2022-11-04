import re
import pandas as pd
import numpy as np

def preprocessTime(data, nameOfTimeColumn):
    pattern = re.compile("\d")
    data[nameOfTimeColumn] = data[nameOfTimeColumn].fillna("0")
    mapping = [((pattern.search(item) is not None)  == False) for item in data[nameOfTimeColumn]]
    data[nameOfTimeColumn][mapping] = "0"
    data[nameOfTimeColumn] = [item.split('/')[-1] for item in data[nameOfTimeColumn]]
    data[nameOfTimeColumn] = [item.split('*')[-1] for item in data[nameOfTimeColumn]]
    data[nameOfTimeColumn] = [item.split('-')[0] for item in data[nameOfTimeColumn]]
    data[nameOfTimeColumn].replace(to_replace="[A-Z]", value="", regex=True)
    pattern3 = re.compile("[a-z]")
    patternSpace = re.compile(" ")
    data[nameOfTimeColumn]= [re.sub(string = item, pattern=pattern3, repl = "") for item in data[nameOfTimeColumn]]
    data[nameOfTimeColumn] = [re.sub(string = item, pattern=patternSpace, repl = "") for item in data[nameOfTimeColumn]]
    return data

def filterTime (maxTime, data, nameOfTimeColumn):
    preprocessTime(data, nameOfTimeColumn)
    filtered_data = data[(data[nameOfTimeColumn].astype(int))<maxTime]
    return filtered_data    