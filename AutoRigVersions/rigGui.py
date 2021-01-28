###########################Rigging With The joints creation also########################################################
#                                                                                                                      #
#                                Auto Rig_V1.0                                                                         #
#                                                                                                                      #
########################################################################################################################

# importing the maya commands as cmds 
import maya.cmds as cmds
import Locators
import Joints

# we are reloading all the extra scripts so that any changes are reloaded
Locators = reload(Locators)
Joints = reload(Joints)

editMode = False


class AutoRigV1():

    def __init__(self):
        self.guiJoints()

    def guiJoints(self):
        global spineCount,neckCount,rig_Type
        if cmds.window (newWindow, q=True, exists =True):
            cmds.deleteUI(newWindow)

        if cmds.windowPref (newWindow, q=True,exists =True):
            cmds.windowPref (newWindow, r=True)
        print
        myGUI = cmds.window (newWindow, t='AutoRig_v1.0', w=500, h=340)
        main_layout =cmds.columnLayout ('Main Header')
        cmds.rowColumnLayout(nc=5, cw=[(1, 150), (2, 100), (3, 100), (4, 100), (5, 50)])
        cmds.separator(h=10, style='none')
        titleDisplay =cmds.text(label = 'Auto Rig V1.0.0',align ="center", font ='boldLabelFont')
        # creating spaces in the GUI
        for i in range(3):
            cmds.separator(h=10,style='none')

        for i in range (5):
            cmds.separator(h=10)

        # naming options (for the creation joints)
        cmds.text ('naming_text',l='Step 1: Set the type of rigs:',fn ='boldLabelFont')
        text2=cmds.text('Rig type Biped or Quadraped',l='Type of Rig:')
        opti=cmds.optionMenu('rig_Menu_Type')
        cmds.menuItem(label='Biped')
        cmds.menuItem(label='Quadraped')

        cmds.button(l='Mirror Loc Y->X', w=10, h=10, c="mirrorLocatorsYX()", aop=True)
        for i in range(1):
            cmds.separator(h=30,style='none')

        for i in range(1):
            cmds.separator(h=30,style='none')


        Locators.globalNames()
        cmds.button(l='Mirror Loc X->Y', w=10, h=10, c="mirrorLocatorsXY()", aop=True)
        for i in range(2):
            cmds.separator(h=30,style='none')

        cmds.text("Neck Count", l="Neck Count:", align="center")
        neckCount = cmds.intField(minValue=1, maxValue=10, value=2)

        cmds.button(l='Edit Mode',w = 10,h=10,c="lockAll(editMode)",aop =True)
        for i in range(2):
            cmds.separator(h=30,style ='none')

        cmds.button(l='Create Locators', c=Locators.generateLocators)
        cmds.button(l='Delete Locators', c=Locators.deleteLocators)

        for i in range(2):
            cmds.separator(h=10,style ='none')

        for i in range(5):
            cmds.separator(h=10)

        cmds.text('step', l='Step 2: Create all the joints  :', fn='boldLabelFont', h=10)

        Joints.CreateJointsWindow()
        '''
        cmds.columnLayout()
        cmds.checkBoxGrp(numberOfCheckBoxes=3, label='Three Buttons', labelArray3=['One', 'Two', 'Three'])
        cmds.checkBoxGrp(numberOfCheckBoxes=4, label='Four Buttons', labelArray4=['I', 'II', 'III', 'IV'])
        '''
        # displaying Window
        cmds.showWindow()

    def lockAll(lock):
        global editMode

        axis =['x','y','z']
        attr = ['t', 'r', 's' ]

        nodes = cmds.listRelatives('Loc_*', allParents =True)

        for axe in axis:
            for att in attr:
                for node in nodes:
                    cmds.setAttr (node +'.' +att+axe, lock= lock)

        if editMode ==False:
            editMode = True
        else:
            editMode = False

    def mirrorLocatorsXY(*args):
        allLeftLocators= cmds.ls("Loc_L*",sl =False)
        leftLocators=cmds.listRelatives(*allLeftLocators,p=True,f=True)
        allRightLocators= cmds.ls("Loc_R*",sl=False)
        rightLocators = cmds.listRelatives(*allRightLocators, p=True, f=True)

        for i,l in enumerate(leftLocators):
            pos = cmds.xform(l, q=True, t =True, ws =True)
            cmds.move(-pos[0],pos[1],pos[2],rightLocators[i])

    def mirrorLocatorsYX(*args):
        allLeftLocators= cmds.ls("Loc_L*",sl =False)
        leftLocators=cmds.listRelatives(*allLeftLocators,p=True,f=True)
        allRightLocators= cmds.ls("Loc_R*",sl=False)
        rightLocators = cmds.listRelatives(*allRightLocators, p=True, f=True)

        for i,l in enumerate(rightLocators):
            pos = cmds.xform(l, q=True, t =True, ws =True)
            cmds.move(-pos[0],pos[1],pos[2],leftLocators[i])