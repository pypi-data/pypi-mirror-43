import tkinter as tk
from PIL import ImageTk
from PIL import Image
from PIL import ImageDraw
import os, shutil
import random
import string
import ntpath

PhotoImage = tk.PhotoImage

SYNXconfigPath = os.path.dirname(__file__)



def shareWithSynx(a,b):
    globals()[a] = b

class Synx():
    root = False
    SynxWHresolve = ''
    baseWidthV = ''
    mediaPath = SYNXconfigPath+'\\media\\gen'
    traverseList = []
    ALL_VARIABLES = {}
    
    def __init__(self,var,root=''):
        if isinstance(root,str):
            self.ALL_VARIABLES[var] = globals()[var]
        else:
            self.ALL_VARIABLES[var] = root
        self.root = self.ALL_VARIABLES[var]
        self.SynxWHresolve = PhotoImage(file=SYNXconfigPath+'/media/vv.png')
        self.cleanUp()

    def cleanUp(self):
        folder = SYNXconfigPath+'/media/gen/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                pass

    def traverse(self,lists):
        if  isinstance(lists,list):
            for item in lists:
                if len(item.winfo_children()) > 0:
                    for item2 in item.winfo_children():
                        if len(item2.winfo_children()) > 0:
                            self.traverse(item2)
                        else:
                            self.traverseList.append(item2)
                else:
                    self.traverseList.append(item)
        else:
            self.traverseList.append(lists)

    def delFromSynx(self,var,clear=False):
        self.traverseList = []
        self.traverse(self.getChild(var).winfo_children())
        parent = None
        for item in self.traverseList:
            if hasattr(item, 'SynxData'):
                if 'image' in item.SynxData:
                    try:
                        os.unlink(item.SynxData['image'])
                    except:
                        pass
                if 'imageVar' in item.SynxData:
                    try:
                        del self.ALL_VARIABLES[item.SynxData['imageVar']]
                    except:
                        pass
                if 'itself' in item.SynxData:
                    try:
                        self.ALL_VARIABLES[item.SynxData['itself']].destroy()
                    except:
                        pass
                    try:
                        del self.ALL_VARIABLES[item.SynxData['itself']]
                    except:
                        pass
        if hasattr(self.getChild(var), 'SynxData'):
                parent = self.getChild(var).SynxData['parent']
        if clear:
            self.ALL_VARIABLES[var].update()
        else:
            if hasattr(self.ALL_VARIABLES[var], 'SynxData'):
                if 'image' in self.ALL_VARIABLES[var].SynxData:
                    try:
                        os.unlink(self.ALL_VARIABLES[var].SynxData['image'])
                    except:
                        pass
                if 'imageVar' in self.ALL_VARIABLES[var].SynxData:
                    try:
                        del self.ALL_VARIABLES[self.ALL_VARIABLES[var].SynxData['imageVar']]
                    except:
                        pass
            try:
                self.ALL_VARIABLES[var].destroy()
            except:
                pass
            try:
                del self.ALL_VARIABLES[var]
            except:
                pass
            if parent:
                try:
                    self.ALL_VARIABLES[parent].update()
                except:
                    pass

    def delImage(self,child):
        if hasattr(child,'SynxData'):
            if 'image' in child.SynxData:
                os.unlink(child.SynxData['image'])
                del self.ALL_VARIABLES[child.SynxData['imageVar']]

    def clearParent(self,parent):
        self.delFromSynx(parent,True)

    def getChild(self,child):
        return self.ALL_VARIABLES[child]

    def affectPlus1(self,point,pointSet,child):
        for i in range(len(point)):
            wid = self.ALL_VARIABLES[child+str(point[i])]
            apply = pointSet[i]
            for key in apply:
                if key == 'style':
                    self.styling(apply[key],wid)
                elif key == 'rounded':
                    defArgs = self.properties(apply[key])
                    widgitIMG = self.rounded(**defArgs)
                    widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                    self.delImage(wid)
                    self.ALL_VARIABLES[child+'widgit'+randP+'Imaged' + str(i)] = PhotoImage(file=widgitIMG)
                    wid.configure(image=self.ALL_VARIABLES[child+'widgit'+randP+'Imaged' + str(i)])
                    wid.SynxData['image'] = widgitIMG
                    wid.SynxData['imageVar'] = child+'widgit'+randP+'Imaged' + str(i)

    def affectPlus2(self,child,fromTo,style,rounded):
        for i in range(fromTo[0],fromTo[1]):
            wid = self.ALL_VARIABLES[child+str(i)]
            if style != '':
                self.styling(style,wid)
            if rounded != '':
                defArgs = self.properties(rounded)
                widgitIMG = self.rounded(**defArgs)
                widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                self.delImage(wid)
                self.ALL_VARIABLES[child+'widgit'+randP+'Imageq' + str(i)] = PhotoImage(file=widgitIMG)
                wid.configure(image=self.ALL_VARIABLES[child+'widgit'+randP+'Imageq' + str(i)])
                wid.SynxData['image'] = widgitIMG
                wid.SynxData['imageVar'] = child+'widgit'+randP+'Imageq' + str(i)

    def affect(self,child='',fromTo='',style='',rounded='',point='',pointSet=''):
        if isinstance(point,list) and isinstance(fromTo,tuple):
            self.affectPlus2(child,fromTo,style,rounded)
            if isinstance(pointSet,list):
                self.affectPlus1(point,pointSet,child)
        elif isinstance(point,list) and not isinstance(fromTo,tuple):
            if isinstance(pointSet,list):
                self.affectPlus1(point,pointSet,child)
        elif isinstance(fromTo,tuple):
            self.affectPlus2(child,fromTo,style,rounded)

    def affectGroup(self,group='',child='',rows=0,columns=0,point=[0],depth=0,style='',styleX=''):
        Cp = 0
        index = 0
        StyleEvery = 0
        if group == 'column':
            maskRow = rows
            maskColumn = columns
            columns = maskRow
            rows = maskColumn
        if group == 'row' or group == 'column':
            for i in range(columns):
                if Cp == len(point):
                    return
                if i == point[Cp]:
                    if group == 'column':
                        start = point[Cp]
                    else:
                        start = index
                    for j in range(depth):
                        wid = self.ALL_VARIABLES[child + str(start)]
                        if isinstance(style,list):
                            for key in style[Cp]:
                                if key == 'style':
                                    self.styling(style[Cp][key],wid)
                                elif key == 'rounded':
                                    defArgs = self.properties(style[Cp][key])
                                    widgitIMG = self.rounded(**defArgs)
                                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                                    widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                                    self.delImage(wid)
                                    self.ALL_VARIABLES[child+'widgitImagez' + str(i) + str(j) + str(randP)] = PhotoImage(file=widgitIMG)
                                    wid.configure(image=self.ALL_VARIABLES[child+'widgitImagez' + str(i) + str(j) + str(randP)])
                                    wid.SynxData['image'] = widgitIMG
                                    wid.SynxData['imageVar'] = child+'widgitImagez' + str(i) + str(j) + str(randP)
                        elif isinstance(styleX,list):
                            for key in styleX[StyleEvery]:
                                if key == 'style':
                                    self.styling(styleX[StyleEvery][key],wid)
                                elif key == 'rounded':
                                    defArgs = self.properties(styleX[StyleEvery][key])
                                    widgitIMG = self.rounded(**defArgs)
                                    widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                                    self.delImage(wid)
                                    self.ALL_VARIABLES[child+'widgitImagev' + str(i) + str(j) + str(randP)] = PhotoImage(file=widgitIMG)
                                    wid.configure(image=self.ALL_VARIABLES[child+'widgitImagev' + str(i) + str(j) + str(randP)])
                                    wid.SynxData['image'] = widgitIMG
                                    wid.SynxData['imageVar'] = child+'widgitImagev' + str(i) + str(j) + str(randP)
                        StyleEvery += 1
                        if group == 'column':
                            start += columns
                        else:
                            start += 1
                    Cp += 1
                index += rows

    def properties(self,rules):
        rules = rules[0:-1]
        rules = dict(e.split('=') for e in rules.split(';'))
        return rules

    def styling(self,rules,child):
        rules = rules[0:-1]
        rules = dict(e.split('=') for e in rules.split(';'))
        child.configure(**rules)

    def fitImage(self,parentSZ,path,per,direct=False):
        basewidth = parentSZ
        basewidth = round((per / 100) * basewidth)
        if direct:
            img = Image.open(path)
            randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            base = ntpath.basename(path)
            path = SYNXconfigPath+'/media/gen/'+randP+base
            img.save(path)
        img = Image.open(path)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        pathNew = path
        img.save(pathNew)
        if direct:
            return PhotoImage(file=pathNew)
        else:
            return pathNew

    def borderRadius(self,im,rad):
        rad = int(rad)
        width, height = im.size
        rad = round((rad / 100) * height)
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def circular(self,im):
        im = im.resize((im.size[1], im.size[1]))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
        return im

    def rounded(self,path='',background='',rad=10,circular=False):
        if circular == False:
            self.baseWidthV = True
        else:
            self.baseWidthV = False
        if path == '':
            if len(list(background)) < 3:
                if circular == False:
                    useMMx = SYNXconfigPath+'/media/vv2.png'
                else:
                    useMMx = SYNXconfigPath+'/media/vv.png'
                im = Image.open(useMMx)
                pixelMap = im.load()
                img = Image.new( im.mode, im.size)
                pixelsNew = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        pixelsNew[i,j] = (255,255,255,255)
                try:
                    rad = int(rad)
                    img = self.borderRadius(img,rad)
                except ValueError:
                    img = self.circular(img)
                randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                base = ntpath.basename(useMMx)
                pathNew = SYNXconfigPath+'/media/gen/'+randP+base
                img.save(pathNew)
                return pathNew
            else:
                if circular == False:
                    useMMx = SYNXconfigPath+'/media/vv2.png'
                else:
                    useMMx = SYNXconfigPath+'/media/vv.png'
                background = background.lstrip('#')
                background = tuple(int(background[i:i+2], 16) for i in (0, 2 ,4))
                im = Image.open(useMMx)
                pixelMap = im.load()
                img = Image.new( im.mode, im.size)
                pixelsNew = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        pixelsNew[i,j] = background
                if circular == False:
                    rad = int(rad)
                    img = self.borderRadius(img,rad)
                else:
                    img = self.circular(img)
                randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                base = ntpath.basename(useMMx)
                pathNew = SYNXconfigPath+'/media/gen/'+randP+base
                img.save(pathNew)
                return pathNew
        else:
            img = Image.open(path)
            if circular == False:
                rad = int(rad)
                img = self.borderRadius(img,rad)
            else:
                img = self.circular(img)
            randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            base = ntpath.basename(path).split('.')[0]+'.png'
            pathNew = SYNXconfigPath+'/media/gen/'+randP+base
            img.save(pathNew)
            return pathNew

    def child_dimensions(self,parent,side,val):
        self.root.update()
        if side == 'w':
            side = parent.winfo_width()
        else:
            side = parent.winfo_height()
        return round((val / 100) * side)

    def resolveSize(self,parent,side,val):
        SynxResolve = tk.Label(self.root,width=1,height=1)
        SynxResolve.grid(column=0,row=0,pady=(2000,0))
        self.root.update()
        if side == 'w':
            width = SynxResolve.winfo_width()
            parentWidth = parent.winfo_width()
            pixWidth = ((width / parentWidth) * 100)
            fin = round((val / pixWidth) * 1)
        else:
            height = SynxResolve.winfo_height()
            parentHeight = parent.winfo_height()
            pixHeight = ((height / parentHeight) * 100)
            fin = round((val / pixHeight) * 1)
        SynxResolve.grid_forget()
        self.root.update()
        return fin

    def layoutWaMa(self,parent,ratioX,rowN):
        padxR = []
        widthxR = []
        widthxResolve = []
        pad = 0
        for i in range(len(ratioX)):
            ratioX[i] = int(ratioX[i])
            padxX = self.child_dimensions(parent,'w',ratioX[i])
            padxR.append(padxX)
            pad += ratioX[i]
        width = 100 - pad
        width = width / rowN
        resolveWval = self.resolveSize(parent,'w',width)
        width = self.child_dimensions(parent,'w',width)
        for i in range(rowN):
            widthxR.append(width)
            widthxResolve.append(resolveWval)
        return [padxR,widthxR,widthxResolve]

    def layoutWsMa(self,parent,widthR):
        widthxR = []
        widthxResolve = []
        widthX = widthR.split(':')
        widthM = 0
        for i in range(len(widthX)):
            widthX[i] = int(widthX[i])
            resolveWval = self.resolveSize(parent,'w',widthX[i])
            width = self.child_dimensions(parent,'w',widthX[i])
            widthxR.append(width)
            widthxResolve.append(resolveWval)
            widthM += widthX[i]
        return [widthM,widthxR,widthxResolve]

    def widget(self,parent,tk,child,attributes):
        parentName = parent
        parent = self.getChild(parent)
        attributes = self.properties(attributes)
        custom = {'path' : None,
                  'background' : None,
                  'circular' : None,
                  'rad' : 0,
                  'style' : None,
                  'id' : None,
                  'event' : None,
                  'class' : None,
                  'animation' : None,
                  'width' : None,
                  'height' : None,
                  'margin-left' : 0,
                  'margin-right' : 0,
                  'margin-top' : 0,
                  'margin-bottom' : 0}
        system = {}
        self.ALL_VARIABLES[child] = tk(parent)
        for attribute in attributes:
            if attribute in custom:
                custom[attribute] = attributes[attribute]
            else:
                system[attribute] = attributes[attribute]
        if custom['width']:
            custom['width'] = self.child_dimensions(parent,'w',int(custom['width']))
            system['width'] = custom['width']
        if custom['height']:
            custom['height'] = self.child_dimensions(parent,'h',int(custom['height']))
            system['height'] = custom['height']
        if custom['margin-left']:
            custom['margin-left'] = self.child_dimensions(parent,'w',int(custom['margin-left']))
        if custom['margin-right']:
            custom['margin-right'] = self.child_dimensions(parent,'w',int(custom['margin-right']))
        if custom['margin-top']:
            custom['margin-top'] = self.child_dimensions(parent,'h',int(custom['margin-top']))
        if custom['margin-bottom']:
            custom['margin-bottom'] = self.child_dimensions(parent,'h',int(custom['margin-bottom']))
        self.ALL_VARIABLES[child].configure(**system)
        self.ALL_VARIABLES[child].grid(column=0,row=0,sticky='nw',pady=(custom['margin-top'],custom['margin-bottom']),padx=(custom['margin-left'],custom['margin-right']))
        self.ALL_VARIABLES[child].SynxData = {'parent' : parentName,'itself' : child}
        if custom['id']:
            self.ALL_VARIABLES[child].SynxData['id'] = custom['id']
        if custom['event']:
            self.ALL_VARIABLES[child].SynxData['event'] = custom['event']
        if custom['class']:
            self.ALL_VARIABLES[child].SynxData['class'] = custom['class']
        if custom['animation']:
            self.ALL_VARIABLES[child].SynxData['animation'] = custom['animation']
        rounded = {}
        if custom['background']:
            if custom['rad']:
                rounded = {'background' : custom['background'], 'rad' : custom['rad']}
            else:
                rounded = {'background' : custom['background'],'circular' : custom['circular']}
        elif custom['path']:
            if custom['rad']:
                rounded = {'path' : custom['path'], 'rad' : custom['rad']}
            else:
                rounded = {'path' : custom['path'],'circular' : custom['circular']}
        if rounded:
            randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            if 'path' in rounded:
                img = Image.open(rounded['path'])
                base = ntpath.basename(rounded['path'])
                path = SYNXconfigPath+'/media/gen/'+randP+base
                img.save(path)
                rounded['path'] = path
                rounded['path'] = self.fitImage(custom['width'],rounded['path'],100)
                widgitIMG = self.rounded(**rounded)
                if rounded['circular']:
                    os.unlink(path)
            else:
                widgitIMG = self.rounded(**rounded)
            self.ALL_VARIABLES[child+'widgitImagez' +  str(randP)] = PhotoImage(file=widgitIMG)
            self.ALL_VARIABLES[child].configure(image = self.ALL_VARIABLES[child+'widgitImagez' +  str(randP)])
            self.ALL_VARIABLES[child].SynxData['image'] = widgitIMG
            self.ALL_VARIABLES[child].SynxData['imageVar'] = child+'widgitImagez' +  str(randP)
            

    def layout(self,parent='win',child='',widget=tk.LabelFrame,sectionN=1,rowN=1,marginXR='auto',widthR='auto',heightR='auto',marginYR='auto',MXdef=5,resolveWH=False,style='',rounded='XXXX'):
        self.ALL_VARIABLES[child] = ''
        parentName = parent
        parent = self.ALL_VARIABLES[parent]
        row = 0
        tick = True
        padxR = []
        widthxR = []
        widthxResolve = []
        heightxResolve = []
        heightxR = []
        heightPad = []

        
        
        for i in range(sectionN):
            if tick:
                row += 1
                tick = False
            elif (i + 1) % rowN == 0:
                tick = True
        
        if widthR == 'auto':
            if marginXR == 'auto':
                marginXR = ''
                for i in range(rowN - 1):
                    marginXR += str(MXdef)+':'
                marginXR = marginXR[0:-1]
                ratioX = marginXR.split(':')
                WaMaRET = self.layoutWaMa(parent,ratioX,rowN)
                padxR = WaMaRET[0]
                widthxR = WaMaRET[1]
                widthxResolve = WaMaRET[2]
            else:
                ratioX = marginXR.split(':')
                WaMaRET = self.layoutWaMa(parent,ratioX,rowN)
                padxR = WaMaRET[0]
                widthxR = WaMaRET[1]
                widthxResolve = WaMaRET[2]
        else:
            if marginXR == 'auto':
                if rowN == 1:
                    rowNX = 2
                else:
                    rowNX = rowN
                widthX = widthR.split(':')
                WsMaRES = self.layoutWsMa(parent,widthR)
                widthM = WsMaRES[0]
                widthxR = WsMaRES[1]
                widthxResolve = WsMaRES[2]
                pmx = 100 - widthM
                pmx = pmx / (rowNX - 1)
                marginXR = ''
                for i in range(rowNX - 1):
                    marginXR += str(round(pmx))+':'
                marginXR = marginXR[0:-1]
                ratioX = marginXR.split(':')
                for i in range(len(ratioX)):
                    ratioX[i] = int(ratioX[i])
                    padxX = self.child_dimensions(parent,'w',ratioX[i])
                    padxR.append(padxX)
            else:
                pad = 0
                ratioX = marginXR.split(':')
                for i in range(len(ratioX)):
                    ratioX[i] = int(ratioX[i])
                    padxX = self.child_dimensions(parent,'w',ratioX[i])
                    padxR.append(padxX)
                    pad += ratioX[i]
                widthX = widthR.split(':')
                WsMaRES = self.layoutWsMa(parent,widthR)
                widthM = WsMaRES[0]
                widthxR = WsMaRES[1]
                widthxResolve = WsMaRES[2]
        
        #____HEIGHTS___________________________________________________________
                    
        if heightR == 'auto':
            if marginYR == 'auto':
                Hpad = MXdef * (row - 1)
                Hpadp = self.child_dimensions(parent,'h',MXdef)
                Hleft = 100 - Hpad
                resolveHval = self.resolveSize(parent,'h',(Hleft / row))
                heigthH = self.child_dimensions(parent,'h',(Hleft / row))
                for i in range(sectionN):
                    if i <= (rowN - 1):
                        heightPad.append([0,heigthH])
                        heightxResolve.append([0,resolveHval])
                    else:
                        heightPad.append([Hpadp,heigthH])
                        heightxResolve.append([Hpadp,resolveHval])
            else:
                marginYR = marginYR.split(':')
                for i in range(len(marginYR)):
                    marginYR[i] = int(marginYR[i])
                    Hpad = marginYR[i] * (row - 1)
                    HpadP = self.child_dimensions(parent,'h',marginYR[i])
                    Hleft = 100 - Hpad
                    resolveHval = self.resolveSize(parent,'h',(Hleft / row))
                    heigthH = self.child_dimensions(parent,'h',(Hleft / row))
                    heightPad.append([HpadP,heigthH])
                    heightxResolve.append([HpadP,resolveHval])
        else:
            if marginYR == 'auto':
                heightR = heightR.split(':')
                for i in range(len(heightR)):
                    heightR[i] = int(heightR[i])
                    resolveHval = self.resolveSize(parent,'h',heightR[i])
                    heigthH = self.child_dimensions(parent,'h',heightR[i])
                    if i <= (rowN - 1):
                        heightPad.append([0,heigthH])
                        heightxResolve.append([0,resolveHval])
                    else:
                        Hpad = MXdef * (row - 1)
                        HpadP = self.child_dimensions(parent,'h',MXdef)
                        heightPad.append([HpadP,heigthH])
                        heightxResolve.append([HpadP,resolveHval])
            else:
                marginYR = marginYR.split(':')
                heightR = heightR.split(':')
                for i in range(len(marginYR)):
                    marginYR[i] = int(marginYR[i])
                    Hpad = marginYR * (row - 1)
                    HpadP = self.child_dimensions(parent,'h',marginYR[i])
                    heightR[i] = int(heightR[i])
                    resolveHval = self.resolveSize(parent,'h',heightR[i])
                    heigthH = self.child_dimensions(parent,'h',heightR[i])
                    heightPad.append([HpadP,heigthH])
                    heightxResolve.append([HpadP,resolveHval])
        indx = 0
        compact = []
        for i in range(rowN):
            compact.append(0)
        for i in range(len(heightPad)):
            mock = heightPad[i][0]
            heightPad[i][0] = heightPad[i][0] + compact[indx]
            compact[indx] += mock + heightPad[i][1]
            if (i + 1) % rowN == 0:
                indx = 0
            else:
                indx += 1

        padx = 0
        pdrC = 0
        widC = 0
        for i in range(sectionN):
            if resolveWH == True:
                useAsWidth = widthxResolve[widC]
                useAsHeight = heightxResolve[i][1]
            else:
                useAsWidth = widthxR[widC]
                useAsHeight = heightPad[i][1]
            self.ALL_VARIABLES[child + str(i)] = widget(parent,width=useAsWidth,height=useAsHeight)
            self.ALL_VARIABLES[child + str(i)].columnconfigure(0,minsize=widthxR[widC])
            self.ALL_VARIABLES[child + str(i)].rowconfigure(0,minsize=heightPad[i][1])
            self.ALL_VARIABLES[child + str(i)].grid(column=0,row=0,sticky='nw',pady=(heightPad[i][0],0),padx=(padx,0))
            self.ALL_VARIABLES[child + str(i)].SynxData = {
                'parent' : parentName,
                'itself' : child + str(i)
                }
            if style != '':
                self.styling(style,self.ALL_VARIABLES[child + str(i)])
            if rounded == 'XXXX':
                pass
            elif rounded.find('background') < 0 and rounded.find('path') < 0 and rounded.find('rad') < 0:
                widgitIMG = self.rounded()
                if self.baseWidthV == True:
                    self.fitImage(widthxR[widC],widgitIMG,100)
                else:
                    self.fitImage(heightPad[i][1],widgitIMG,100)
                self.ALL_VARIABLES[child+'widgitImage' + str(i)] = PhotoImage(file=widgitIMG)
                self.ALL_VARIABLES[child + str(i)].configure(image=self.ALL_VARIABLES[child+'widgitImage' + str(i)])
                self.ALL_VARIABLES[child + str(i)].SynxData['image'] = widgitIMG
                self.ALL_VARIABLES[child + str(i)].SynxData['imageVar'] = child+'widgitImage' + str(i)
            else:
                defArgs = self.properties(rounded)
                widgitIMG = self.rounded(**defArgs)
                if self.baseWidthV == True:
                    self.fitImage(widthxR[widC],widgitIMG,100)
                else:
                    self.fitImage(heightPad[i][1],widgitIMG,100)
                self.ALL_VARIABLES[child+'widgitImage' + str(i)] = PhotoImage(file=widgitIMG)
                self.ALL_VARIABLES[child + str(i)].configure(image=self.ALL_VARIABLES[child+'widgitImage' + str(i)])
                self.ALL_VARIABLES[child + str(i)].SynxData['image'] = widgitIMG
                self.ALL_VARIABLES[child + str(i)].SynxData['imageVar'] = child+'widgitImage' + str(i)
            if (i + 1) % rowN == 0 :
                pdrC = 0
                widC = 0
                padx = 0
            else:
                padx += widthxR[widC] + padxR[pdrC]
                pdrC += 1
                widC += 1
