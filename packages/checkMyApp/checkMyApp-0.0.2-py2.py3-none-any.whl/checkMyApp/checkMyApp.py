#!/usr/bin/env python

import setuptools
import sys
import json
import ast
import os
import re
from check_manifest import check_manifest
from pyflakes import api as pyflask_api
from pyflakes import reporter as modReporter
import pkgutil

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

pythonVar = "{0}.{1}".format(sys.version_info[0], sys.version_info[1])


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ignore data from setup.py
ignoreList = [
    'import setup',
    'rm ',
    'find_packages',
    'mv '
]

finalReport = ''
stopReporting = False


def setup(**kwargs):
    print(kwargs)

def read_setuppy_file():
    setuppy = ""
    excludedNonCompiled=set()

    # replace setuptool's setup function with our own
    setuptools.setup = setup

    with open('setup.py') as content:
        for line in content:
            for ignoreItem in ignoreList:
                if ignoreItem in line:
                    excludedNonCompiled.add(line)
                    break
            else:
                setuppy += line

    return [setuppy, list(excludedNonCompiled)]

def getSetup():
    """ get and run code in setup.py """
    setuppy = read_setuppy_file()[0]
    excludedLines = read_setuppy_file()[1]

    codeOut = StringIO()

    sys.stdout = codeOut
    tempfile = {}
    try:
        exec (setuppy, globals())
    except:
        pass
    sys.stdout = sys.__stdout__
    result = codeOut.getvalue()
    codeOut.close()

    return [result, sys.exc_info()[1], excludedLines]


def validate_setupfile_structure():
    """ parses setupfile into json """

    # search for setup.py, throw error if not exists
    if not os.path.isfile('setup.py'):
        print ("{} Couldn't find setup.py file, please run the script from the same folder in which setup.py resides."
               " {}".format(bcolors.FAIL, bcolors.ENDC))
        exit(1)
    with open('setup.py', 'r') as setupfile:
        lines = setupfile.readlines()
        joindFile = "".join(lines)

        # Check if we have a setup file (checking for the setup(*))
        try:
            re.search(r'setup\([^*]*\)', joindFile).group(0)
        except AttributeError:
            print ("{0} Couldn't file setup(*) structure inside the file, is this really a setup.py file? {1}"
                   .format(bcolors.FAIL, bcolors.ENDC))
            exit(1)
        else:
            return True


def run_pyflakes():
    """ check if the code wer'e about to import is fine"""
    returnSTRM = StringIO()
    reporter = modReporter.Reporter(returnSTRM, returnSTRM)
    with open("setup.py", "r") as file:
        pyflask_api.check(file.read(), 'line', reporter)

    output = returnSTRM.getvalue()
    returnSTRM.close()

    return output


def checkIfValueExists(**kwargs):
    setupJsonVar = kwargs.get('setupJson')
    value = kwargs.get('value')

    try:
        setupJsonVar[value]
    except KeyError:
        return False
    else:
        return True


def import_test(**kwargs):
    module_name = kwargs.get('module')
    func = kwargs.get('func', None)
    sys.path.insert(0, '{}'.format(os.getcwd()))

    if func is not None:
        try:
            new_module = __import__(module_name)
        except ImportError:
            return False
        else:
            if hasattr(new_module, func):
                return True
            else:
                return False
    else:
        try:
            pkgutil.find_loader(module_name)
        except ImportError:
            return False
        else:
            if pkgutil.find_loader(module_name) is not None:
                return True
            else:
                return False


def check_declared_packages(**kwargs):
    setupJsonVar = kwargs.get('setupJson')
    fileList = kwargs.get('fileList')
    global finalReport

    if not checkIfValueExists(setupJson=setupJsonVar, value='packages'):
        finalReport += "*\t{0}Couldn't find MUST HAVE configuration in setup.py: packages{1}\n".format(bcolors.FAIL,
                                                                                                       bcolors.ENDC)
        stopReporting = True
        return False

    noPackages = []
    initPackages = []
    if setupJsonVar['packages'] == 'find_packages()':
        return True
    else:
        packageDict = ast.literal_eval(json.dumps(setupJsonVar['packages']))
        # Check if declared modules can be loaded
        for package in packageDict:
            if not import_test(module=package):
                noPackages.append(package)

        # Check if folders with __init__.py are not declared as modules
        for package in fileList:
            if package not in packageDict:
                initPackages.append(package)

        if noPackages:
            finalReport += "*\t{0}Couldn't import the package(s): {1}\n".format(bcolors.FAIL, bcolors.ENDC)

            for package in noPackages:
                finalReport += "\t\t{0}{1}{2}\n".format(bcolors.FAIL, package, bcolors.ENDC)
            stopReporting = True

        if initPackages:
            finalReport += "*\t{0}The following folder(s) have __init__.py but not declared as module: {1}\n".format(
                bcolors.FAIL, bcolors.ENDC)

            for package in initPackages:
                finalReport += "\t\t{0}{1}{2}\n".format(bcolors.FAIL, package, bcolors.ENDC)
            stopReporting = True

        finalReport += (
            "*\t{}packages are not declared with 'find_packages()'{}\n".format(bcolors.WARNING, bcolors.ENDC))
        return False

def run_check_menifest():
    codeOut = StringIO()
    codeErr = StringIO()
    sys.stdout = codeOut
    sys.stderr = codeErr
    check_manifest(update=True)
    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    with open("check_manifest.log", "w+") as file:
        file.write(codeErr.getvalue())
    codeOut.close()
    codeErr.close()


class GetOutOfLoop(Exception):
    pass


def main():
    global finalReport, stopReporting

    print ('\n{0}{1}CheckMyApp report for python packaging {2}'.format(bcolors.HEADER, bcolors.UNDERLINE, bcolors.ENDC))
    print ("Legend:\t{0}Warning{1}\t\tError{2}\t\tOK{3}\n".format(bcolors.WARNING, bcolors.FAIL, bcolors.OKGREEN,
                                                                  bcolors.ENDC))
    concent = False
    try:
        while not concent:
            text = "{}Please note:\n" \
                   "This tools uses python's 'exec' function in order to parse setup.py\n" \
                   "This can be dangerous if you'r not familiar with the code inside setup.py.\n\n" \
                   "Please approve the usage of the tool by typing 'yes' (or CTRL+c to cancel){}: " \
                .format(bcolors.WARNING, bcolors.ENDC)

            if pythonVar == "2.7":
                userInput = raw_input(text)
            else:
                userInput = input(text)
            concent = True if userInput == "yes" else False

    except KeyboardInterrupt:
        print("{}Chao!{}".format(bcolors.OKGREEN, bcolors.ENDC))
        exit(1)

    if validate_setupfile_structure():
        py_output = run_pyflakes()
        if py_output != "":
            print("\n\n{0}{4}SETUP.PY ERRORS!!{1}\n"
                  "{2}Before we can continue, you need to fix the following in your setup.py file:\n"
                  "{3}{1}".format(bcolors.HEADER, bcolors.ENDC, bcolors.FAIL, py_output, bcolors.UNDERLINE))
        else:
            setupRaw = getSetup()
            if (setupRaw[1] != "") and (setupRaw[1] is not None):
                print("{0}Cannot continue! I encountered the following error while trying to compile setup.py:\n"
                      "{1}\n\nExiting.. {2}".format(bcolors.FAIL, setupRaw[1], bcolors.ENDC))
                exit(1)
            else:
                try:
                    setupJson = ast.literal_eval(getSetup()[0])
                except SyntaxError:
                    print("{0}Got syntax error while parsing setup.py, exiting.. {1}".format(bcolors.FAIL, bcolors.ENDC))
                    exit(1)
                else:
                    try:
                        for line in getSetup()[2]:
                            # Special reference for find_packages which should be re-added without compiling to the setup.py json file
                            if ('import' in line) and ('find_packages' in line):
                                setupJson['packages'] = "find_packages()"
                    except KeyError:
                        pass

                    # Get current folder's file list, the check if declared modules in setup.py are actual python modules,
                    #    Plus, verify that there are no modules forgotten from setup.py registrations
                    fileList = ['.'.join(x[0].split('/')[-len(x):][1:]) for x in os.walk('.') if
                                (x[0] != '.') and ('__init__.py' in x[2])]
                    check_declared_packages(fileList=fileList, setupJson=setupJson)

                    # Check for 'must have' values
                    missingTagsList = []
                    requiredValues = ['name', 'version', 'author', 'author_email', 'description', 'url', 'install_requires']

                    for value in requiredValues:
                        if not checkIfValueExists(setupJson=setupJson, value=value):
                            missingTagsList.append(value)

                    if missingTagsList:
                        finalReport += "*\t{0}Required tags are missing: {1}{2}\n".format(bcolors.FAIL, missingTagsList,
                                                                                          bcolors.ENDC)
                        stopReporting = True

                    ''' Verify that all required packages indeed exists '''
                    missingRequired = []
                    if checkIfValueExists(setupJson=setupJson, value='install_requires'):
                        for required in setupJson['install_requires']:
                            if not import_test(module=required):
                                missingRequired.append(required)
                        if missingRequired:
                            finalReport += "*\t{0}{3}Couldn't load the following requirements{2}{0}:\n {1}\t{0}\n\n(This means that the " \
                                           "modules doesn't exists in the machine you'r running the script on " \
                                           "it doesn't necessary means that the package won't after packaging.{2}\n\n" \
                                .format(bcolors.WARNING, missingRequired, bcolors.ENDC, bcolors.UNDERLINE)

                # Verify that entry_points does exists and work
                entryPointErrors = []
                entryPointsDict = {}
                missingModulesInEntryPointes = set()
                if checkIfValueExists(setupJson=setupJson, value='entry_points'):
                    for entry in setupJson['entry_points']['console_scripts']:
                        splitted_entry = entry.split('=')
                        entryPointsDict[splitted_entry[0]] = splitted_entry[1]

                    for keys, entryPath in entryPointsDict.items():
                        try:
                            entryPath.split(':')[1]
                        except IndexError:
                            finalReport += "*\t{}Method name is missing for entry point: {}\n\t(define by ':', for example: " \
                                           "path.to.module:def{}\n".format(bcolors.FAIL, entryPath, bcolors.ENDC)
                            stopReporting = True
                        else:
                            moduleName = entryPath.split(':')[0].strip(' ')
                            defName = entryPath.split(':')[1].strip(' ')

                            if import_test(module=moduleName):
                                pathToFile = ('{}.py'.format(entryPath.split(':')[0].replace('.', '/')).strip(' '))
                                if os.path.isfile(pathToFile):
                                    with open(pathToFile, 'r') as entryPathFile:
                                        data = entryPathFile.read()
                                        searchTerm = r'def ' + defName + r'\(.*\):\n'
                                        try:
                                            re.search(searchTerm, data, re.MULTILINE).group(0)
                                        except AttributeError:
                                            entryPointErrors.append(
                                                "Couldn't find method named {0} in {1}".format(defName, pathToFile))
                                else:
                                    entryPointErrors.append("Couldn't find file {}".format(pathToFile))
                            else:
                                missingModulesInEntryPointes.add("{}".format(moduleName))

                if entryPointErrors:
                    finalReport += "*\t{0} EntryPoint error(s): {1}\n".format(bcolors.FAIL, bcolors.ENDC)
                    for error in entryPointErrors:
                        finalReport += "\t\t{0}{1}{2}\n".format(bcolors.FAIL, error, bcolors.ENDC)
                    stopReporting = True
                if missingModulesInEntryPointes:
                    finalReport += "*\t{0}EntryPoint error: The following module/s Couldn't be imported in order to entry_points " \
                                   "to work: {1}{2}\n".format(bcolors.FAIL, list(missingModulesInEntryPointes),
                                                              bcolors.ENDC)
                    stopReporting = True

                # Check what install_requires not used in the code
                requiredModules = set()
                notUsedRequired = set()
                for module in setupJson['install_requires']:
                    if "==" in module:
                        notFoundModule = module.split("==")[0]
                    try:
                        for root, dirs, files in os.walk("."):
                            for file in files:
                                if file.endswith(".py"):
                                    try:
                                        if notFoundModule in open(os.path.join(root, file)).read():
                                            raise GetOutOfLoop
                                    except UnicodeDecodeError:
                                        pass

                    except GetOutOfLoop:
                        requiredModules.add(module)
                        pass
                    else:
                        notUsedRequired.add(notFoundModule)

                if notUsedRequired:
                    finalReport += "*\t{0}{3}The following module(s) seems to be required under 'install_requires' but not in use in the code{1}{0}:\n\t{2}{1}\n".format(
                        bcolors.FAIL, bcolors.ENDC, notUsedRequired, bcolors.UNDERLINE)
                    stopReporting = True
                if requiredModules and notUsedRequired:
                    finalReport += "*\t{0}Alternatively, you can replace you required module list with the following:\n\t{2}{1}\n".format(
                        bcolors.OKGREEN, bcolors.ENDC, list(requiredModules))
                    stopReporting = True

                ## Remove '#' for debug
                # print (json.dumps(setupJson, indent=4, separators=(',', ': '), sort_keys=True))

                # Check if declared module name equals to containing folder name, otherwise can cause errors in automatic deployment pipelines
                parentFolder = os.getcwd()[::-1].split('/')[0][::-1]
                if setupJson['name'] != parentFolder:
                    finalReport += "*\t{0}{3}Declared module name ('{2}') is different from containing folder name('{3}'), please fix{1}\n".format(
                        bcolors.FAIL, bcolors.ENDC, setupJson['name'], parentFolder)
                    stopReporting = True

                if not finalReport:
                    print ("{0}Nothing to report, Amazing! all good!{1}".format(bcolors.OKGREEN, bcolors.ENDC))
                else:
                    print (finalReport)

                if stopReporting:
                    return False
                else:
                    print (
                        '{0}Very well!!, the report did find some issue that you should probebly fix, but nothing that should stop us from releasing the module. '.format(
                            bcolors.OKGREEN, bcolors.ENDC))
                    print (
                        '{0}Report done, running check_manifest tool to create MANIFEST.in and egg file, log is avaliable at check_manifest.log'.format(
                            bcolors.HEADER, bcolors.ENDC))

                    run_check_menifest()
