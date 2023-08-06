import tarfile
import re
import sys
import os

def extractPackage(packagePath):
  """
  Extracts a .unitypackage into the current directory
  @param {string} packagePath The path to the .unitypackage
  """
  with tarfile.open(name=packagePath) as upkg:
    for name in upkg.getnames():
      if re.search(r"[/\\]", name): #Only the top level files of the tar
        continue

      try:
        upkg.getmember(f"{name}/pathname")
        upkg.getmember(f"{name}/asset")
      except KeyError:
        continue #Doesn't have the required files to extract it

      #Extract the path name of the asset
      pathname = upkg.extractfile(f"{name}/pathname").readline() #Reads the first line of the pathname file
      pathname = pathname[:-1].decode("utf-8") #Remove the newling, and decode
      #Extract to the pathname
      print(f"Extracting '{name}' as '{pathname}'")
      assetFile = upkg.extractfile(f"{name}/asset")
      os.makedirs(os.path.dirname(pathname), exist_ok=True) #Make the dirs up to the given folder
      open(pathname, "wb").write(assetFile.read())          #Write out to our own named folder

if __name__ == "__main__":
  extractPackage(sys.argv[1])