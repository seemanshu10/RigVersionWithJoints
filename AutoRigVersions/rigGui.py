###########################Rigging With The joints creation also########################################################
#                                                                                                                      #
#                                Auto Rig_V1.0                                                                         #
#                                                                                                                      #
########################################################################################################################

# importing the maya commands as cmds 
import maya.cmds as cmds
#import Locators
#Locators=reload(Locators)

scriptName = __name__
newWindow = 'Auto_rigMaker'
editMode = False

def guiJoints():

    global spineCount,neckCount
    if cmds.window (newWindow, q=True, exists =True):
        cmds.deleteUI(newWindow)

    if cmds.windowPref (newWindow, q=True,exists =True):
        cmds.windowPref (newWindow, r=True)

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
    for i in range(2):
        cmds.separator(h=30,style='none')

    cmds.text("Spine Count",l="Spine Count:",align ="center")
    spineCount = cmds.intField(minValue=1, maxValue=10, value=4)
    cmds.button(l='Mirror Loc X->Y', w=10, h=10, c="mirrorLocatorsXY()", aop=True)
    for i in range(2):
        cmds.separator(h=30,style='none')

    cmds.text("Neck Count", l="Neck Count:", align="center")
    neckCount = cmds.intField(minValue=1, maxValue=10, value=2)

    cmds.button(l='Edit Mode',w = 10,h=10,c="lockAll(editMode)",aop =True)
    for i in range(2):
        cmds.separator(h=30,style ='none')

    cmds.button(l='Create Locators', c=generateLocators)
    cmds.button(l='Delete Locators', c=deleteLocators)

    for i in range(2):
        cmds.separator(h=10,style ='none')

    for i in range(5):
        cmds.separator(h=10)

    cmds.text('step', l='Step 2: Create all the joints  :', fn='boldLabelFont', h=10)

    cmds.button(l='Create Joints ', c=createJoints)
    '''
    cmds.columnLayout()
    cmds.checkBoxGrp(numberOfCheckBoxes=3, label='Three Buttons', labelArray3=['One', 'Two', 'Three'])
    cmds.checkBoxGrp(numberOfCheckBoxes=4, label='Four Buttons', labelArray4=['I', 'II', 'III', 'IV'])
    '''
    # displaying Window
    cmds.showWindow()

def createJoints(*args):
    if cmds.objExists("Rig"):
        print "Rig already Exists"
    else:
        jointGrp = cmds.group(em =True, name ="Rig")

    #create spine
    root =cmds.ls("Loc_ROOT")
    allSpine= cmds.ls ("Loc_SPINE_*",type ='locator')
    spine= cmds.listRelatives(*allSpine, p =True,f=True)
    rootPos = cmds.xform(root, q=True,t =True,ws =True)

    #create spine
    for i,j in enumerate(spine):
        pos = cmds.xform(j, q =True, t =True, ws =True)
        j= cmds.joint(radius =2,p=pos,name ="Rig_Spine_"+str(i))

    #create Arm

    L_upperArm = cmds.ls('Loc_LeftArm_0')
    L_UpperArmPos = cmds.xform(L_upperArm, q=True, t=True,ws =True)
    L_upperArmJoint = cmds.joint(radius =0.5,p = L_UpperArmPos,name ="Rig_L_UpperArm0")

    L_upperArm = cmds.ls('Loc_LeftArm_1')
    L_UpperArmPos = cmds.xform(L_upperArm, q=True, t=True, ws=True)
    L_upperArmJoint = cmds.joint(radius=0.5, p=L_UpperArmPos, name="Rig_L_UpperArm1")
    
    L_upperArm = cmds.ls('Loc_LeftArm_2')
    L_UpperArmPos = cmds.xform(L_upperArm, q=True, t=True, ws=True)
    L_upperArmJoint = cmds.joint(radius=0.5, p=L_UpperArmPos, name="Rig_L_UpperArm2")

    # mirror joint
    cmds.mirrorJoint( 'Rig_L_UpperArm0',mirrorYZ =True, searchReplace=('L_', 'R_'))
    '''
    for i range (0,3):
        L_upperArm = cmds.ls('Loc_LeftArm_'+str(i))
        #L_upperArmPos = cmds.xform(L_upperArm, q=True, t=True, ws=True)
        #print (L_upperArmPos)
        #L_upperArmJoint = cmds.joint(radius=0.5, p=L_UpperArmPos, name="RIG_L_UpperArm"+str(i))
    '''

def generateLocators(*args):
    if cmds.objExists("LOC_Master"):
        print
        'Joints Master already exists.'
    else:
        cmds.group(em=True, name='LOC_Master')
    root = cmds.spaceLocator(n="LOC_ROOT")
    cmds.scale(0.5, 0.5, 0.5, root)
    cmds.move(0, 1, 0, root)
    cmds.parent(root, "LOC_Master")
    createSpine()

def createSpine():
    global rig_Type
    rig_Type = cmds.optionMenu('rig_Menu_Type', q=True, sl=True)
    for i in range(0, cmds.intField(spineCount, q=True, value=True)):
        spine = cmds.spaceLocator(n='Loc_SPINE_' + str(i))
        cmds.move(0, (4 * i), 0, spine)
        # cmds.parent(spine,'LOC_ROOT')
        if i == 0:
            cmds.parent(spine, 'LOC_ROOT')
        else:
            cmds.parent(spine, 'Loc_SPINE_' + str(i - 1))

    if rig_Type == 1:
        cmds.move(0, 20, 0, 'LOC_Master')
    if rig_Type == 2:
        cmds.rotate(90, 0, 0, 'LOC_Master')
        cmds.move(0, 10, -6, 'LOC_Master')

    createArms(1)
    createArms(-1)
    createLegs(1)
    createLegs(-1)
    createHead()

def createHead():

    for i in range(0, cmds.intField(neckCount, q=True, value=True)):
        neck = cmds.spaceLocator(n='Loc_Neck_' + str(i))
        cmds.move(0, (3 * i), 0, neck)
        if i == 0:
            cmds.parent(neck, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
        else:
            cmds.parent(neck, 'Loc_Neck_' + str(i - 1))

    if rig_Type == 1:
        cmds.move(0,37,0,'Loc_Neck_' + str(i))
    if rig_Type == 2:
        cmds.rotate(180, 0, 0, 'Loc_Neck_' + str(i))
        cmds.move(0, 10, -6, 'Loc_Neck_' + str(i))


def createArms(side):
    rig_Type = cmds.optionMenu('rig_Menu_Type', q=True, sl=True)
    if rig_Type == 1:
        if side == 1:  # for Left_arm
            if cmds.objExists("L_Arm_GRP"):
                print
                "is not doing anything"
            else:
                L_arm = cmds.group(em=True, name='L_Arm_GRP')
                cmds.parent(L_arm, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(4 * side, 1 + (8 * cmds.intField(spineCount, query=True, value=True)), 0, L_arm)
                # upper Arm joints
                for i in range(0, 3):
                    upperArm = cmds.spaceLocator(n='Loc_LeftArm_' + str(i))
                    cmds.move((8 * i), 0, 0, upperArm, preserveChildPosition=False)

                    if i == 0:
                        cmds.parent(upperArm, L_arm)
                    else:
                        cmds.parent(upperArm, 'Loc_LeftArm_' + str(i - 1))

                tempConst = cmds.parentConstraint(L_arm, 'Loc_LeftArm_' + str(0), mo=False)
                cmds.delete(tempConst)

        else:
            # for Right_arm
            if cmds.objExists('R_Arm_GRP'):
                print
                "is not doing anything"
            else:
                R_arm = cmds.group(em=True, name='R_Arm_GRP')
                cmds.parent(R_arm, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(4 * side, 1 + (8 * cmds.intField(spineCount, query=True, value=True)), 0, R_arm)
                # upper Arm joints
                for i in range(0, 3):
                    upperArm = cmds.spaceLocator(n='Loc_RightArm_' + str(i))
                    cmds.move((-8 * i), 0, 0, upperArm)

                    if i == 0:
                        cmds.parent(upperArm, R_arm)
                    else:
                        cmds.parent(upperArm, 'Loc_RightArm_' + str(i - 1))
                tempConst = cmds.parentConstraint(R_arm, 'Loc_RightArm_' + str(0), mo=False)
                cmds.delete(tempConst)
    else:
        if side == 1:  # for Left_Leg
            if cmds.objExists("L_Leg_Front_GRP"):
                print
                "is not doing anything"
            else:
                L_leg_front = cmds.group(em=True, name='L_Leg_Front_GRP')
                cmds.parent(L_leg_front, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2 * side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), -7, L_leg_front, r=1)

                # Create the locators left leg
                for i in range(0, 3):
                    front_Locator = cmds.spaceLocator(n='L_Leg_front_' + str(i))
                    cmds.move(2, (-4 * i), -6, front_Locator)  # (5 * i)

                    if i == 0:
                        cmds.parent(front_Locator, L_leg_front)
                    else:
                        cmds.parent(front_Locator, 'L_Leg_front_' + str(i - 1))

                tempConst = cmds.parentConstraint(L_leg_front, 'L_Leg_front_' + str(0), mo=False)
                cmds.delete(tempConst)


        else:  # for Right_leg front
            if cmds.objExists('R_Leg_Front_GRP'):
                print
                "is not doing anything"
            else:
                R_leg_front = cmds.group(em=True, name='R_Leg_Front_GRP')
                cmds.parent(R_leg_front, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2 * side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), -7, R_leg_front, r=1)

                # Create the locators right leg
                for i in range(0, 3):
                    front_Locator = cmds.spaceLocator(n='R_Leg_front_' + str(i))
                    cmds.move(-2, (-4 * i), -6, front_Locator)

                    if i == 0:
                        cmds.parent(front_Locator, R_leg_front)
                    else:
                        cmds.parent(front_Locator, 'R_Leg_front_' + str(i - 1))

                tempConst = cmds.parentConstraint(R_leg_front, 'R_Leg_front_' + str(0), mo=False)
                cmds.delete(tempConst)


def createLegs(side):
    rig_Type = cmds.optionMenu('rig_Menu_Type', q=True, sl=True)
    if rig_Type == 1:
        if side == 1:  # for Left_Leg
            if cmds.objExists("L_Leg_GRP"):
                print
                "is not doing anything"
            else:
                L_leg = cmds.group(em=True, name='L_Leg_GRP')
                cmds.parent(L_leg, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(4 * side, 1 + (4 * cmds.intField(spineCount, query=True, value=True)), 0, L_leg)
                # upper Arm joints
                for i in range(0, 3):
                    upperLeg = cmds.spaceLocator(n='Loc_LeftLeg_' + str(i))
                    cmds.move(0, (-8.5 * i), 0, upperLeg, preserveChildPosition=False)

                    if i == 0:
                        cmds.parent(upperLeg, L_leg)
                    else:
                        cmds.parent(upperLeg, 'Loc_LeftLeg_' + str(i - 1))

                tempConst = cmds.parentConstraint(L_leg, 'Loc_LeftLeg_' + str(0), mo=False)
                cmds.delete(tempConst)

        else:  # for Right_leg
            if cmds.objExists('R_Leg_GRP'):
                print
                "is not doing anything"
            else:
                R_leg = cmds.group(em=True, name='R_Leg_GRP')
                cmds.parent(R_leg, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(4 * side, 1 + (4 * cmds.intField(spineCount, query=True, value=True)), 0, R_leg)
                # upper Arm joints
                for i in range(0, 3):
                    upperLeg = cmds.spaceLocator(n='Loc_RightLeg_' + str(i))
                    cmds.move(0, (-8.5 * i), 0, upperLeg)
                    if i == 0:
                        cmds.parent(upperLeg, R_leg)
                    else:
                        cmds.parent(upperLeg, 'Loc_RightLeg_' + str(i - 1))
                tempConst = cmds.parentConstraint(R_leg, 'Loc_RightLeg_' + str(0), mo=False)
                cmds.delete(tempConst)
    else:
        if side == 1:  # for Left_Leg_Back
            if cmds.objExists("L_Leg_Back_GRP"):
                print
                "is not doing anything"
            else:
                L_leg_back = cmds.group(em=True, name='L_Leg_Back_GRP')
                cmds.parent(L_leg_back, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2 * side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), 8, L_leg_back, r=1)

                # Create the locators left leg
                for i in range(0, 3):
                    back_Locator = cmds.spaceLocator(n='L_Leg_Back_' + str(i))
                    cmds.move(2, (4 * -i), 8, back_Locator)  # (5 * i)

                    if i == 0:
                        cmds.parent(back_Locator, L_leg_back)
                    else:
                        cmds.parent(back_Locator, 'L_Leg_Back_' + str(i - 1))

                tempConst = cmds.parentConstraint(L_leg_back, 'L_Leg_Back_' + str(0), mo=False)
                cmds.delete(tempConst)

        else:  # for Right_leg_Back

            if cmds.objExists('R_Leg_Back_GRP'):
                print
                "is not doing anything"
            else:
                R_leg_back = cmds.group(em=True, name='R_Leg_Back_GRP')
                cmds.parent(R_leg_back, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2 * side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), 8, R_leg_back, r=1)

                # Create the locators right leg
                for i in range(0, 3):
                    back_Locator = cmds.spaceLocator(n='R_Leg_Back_' + str(i))
                    cmds.move(-2, (4 * -i), 8, back_Locator)

                    if i == 0:
                        cmds.parent(back_Locator, R_leg_back)
                    else:
                        cmds.parent(back_Locator, 'R_Leg_Back_' + str(i - 1))

                tempConst = cmds.parentConstraint(R_leg_back, 'R_Leg_Back_' + str(0), mo=False)
                cmds.delete(tempConst)


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

def deleteLocators(*args):
    loc=cmds.ls ('LOC_*',sl =False)
    cmds.delete(loc)
    temp=cmds.ls('Rig')
    cmds.delete(temp)
