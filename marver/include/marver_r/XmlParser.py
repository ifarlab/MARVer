import xml.etree.ElementTree as ET
from include.marver_r.XmlTemplate import XmlTemplate
import re


class XmlParser:
    def __init__(self, fileName):
        self.__tree = ET.parse(fileName)
        self.__root = self.__tree.getroot()
        self.__globalVariables = self.__getVariablesFromDeclaration(self.__root.find("declaration").text)
        self.__templates = []
        self.__queries = []

        for temp in self.__root.findall("template"):
            tempTemplate = XmlTemplate(temp.find("name").text)

            for location in temp.findall("location"):
                if location.findall("name"):
                    tempTemplate.addNode(location.findall("name")[0].text)
                else:
                    tempTemplate.addNode("Unknown")

            if temp.find("declaration") is not None:
                tempTemplate.setVariables(self.__getVariablesFromDeclaration(temp.find("declaration").text))

            self.__templates.append(tempTemplate)

        for queries in self.__root.findall("queries"):
            for query in queries.findall("query"):
                for formula in query.findall("formula"):
                    self.__queries.append(formula.text.strip())

    @staticmethod
    def __getVariablesFromDeclaration(declaration):
        lines = declaration.split('\n')
        lines = [i.strip() for i in lines if i[:2] != "//"]
        declaration = ' '.join(lines).replace("\t", " ")
        brMap = []
        i = 0
        while True:
            if i >= declaration.__len__():
                break
            if declaration[i] == '{':
                brMap.append(i)
            elif declaration[i] == '}':
                if brMap:
                    declaration = declaration[: brMap[-1]:] + " val " + declaration[i + 1::]
                    i = brMap[-1] + 4
                    brMap = brMap[:-1]
            i += 1

        if re.findall('\[(.+?)\]', declaration):
            res = re.findall('\[(.+?)\]', declaration)
            for item in res:
                if ',' in item:
                    declaration = declaration.replace(item, ' val ')

        lines = declaration.split(';')
        for i in range(lines.__len__()):
            if "=" in lines[i]:
                lines[i] = lines[i].split('=')[0].strip()
            if lines[i][-5:] == " val ":
                lines[i] = ""
            if ',' in lines[i]:
                multiVar = lines[i].split(',')
                for ln in multiVar:
                    lines.append(ln.strip().split(' ')[-1].split("[")[0])
                lines[i] = ""
            else:
                lines[i] = lines[i].strip().split(' ')[-1].split("[")[0]

        return list(set([i for i in lines if i]))

    def getVariables(self):
        return self.__globalVariables

    def getTemplates(self):
        return self.__templates

    def getQueries(self):
        return self.__queries

