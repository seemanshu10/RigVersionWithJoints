import maya.cmds as cmds
import Locators

Locators =reload(Locators)

def CreateJointsWindow():
	#global spineCount 
	#cmds.button(l='Create Joints ', c="Joints.createJoints()")
	#spineCount = cmds.intField(minValue=1, maxValue=10, value=4)
	print "i print"
	
def createJoints():
    if cmds.objExists("Rig"):
        print "Rig already Exists"
    else:
        jointGrp = cmds.group(em =True, name ="Rig")
    
    global rig_Type
    rig_Type = cmds.optionMenu('rig_Menu_Type', q=True, sl=True)
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
    # create biped
    if rig_Type == 1:
        # left arm
        L_upperArm = cmds.ls('Loc_LeftArm_0')
        L_UpperArmPos = cmds.xform(L_upperArm, q=True, t=True,ws =True)
        L_upperArmJoint = cmds.joint(radius =0.5,p = L_UpperArmPos,name ="Rig_L_UpperArm0")

        L_upperArm = cmds.ls('Loc_LeftArm_1')
        L_UpperArmPos = cmds.xform(L_upperArm, q=True, t=True, ws=True)
        L_upperArmJoint = cmds.joint(radius=0.5, p=L_UpperArmPos, name="Rig_L_UpperArm1")

        L_upperArm = cmds.ls('Loc_LeftArm_2')
        L_UpperArmPos = cmds.xform(L_upperArm, q=True, t=True, ws=True)
        L_upperArmJoint = cmds.joint(radius=0.5, p=L_UpperArmPos, name="Rig_L_UpperArm2")

        #create leg
        cmds.select(d=True)
        cmds.select('Rig_Spine_0')

        L_upperLegJoint = cmds.joint(radius =1,p=cmds.xform(cmds.ls('Loc_LeftLeg_0', type ='transform'), q=True,t= True, ws =True), name ="Rig_L_Leg_0")
        L_upperLegJoint1 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('Loc_LeftLeg_1', type='transform'), q=True, t=True, ws=True),name="Rig_L_Leg_1")
        L_upperLegJoint2 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('Loc_LeftLeg_2', type='transform'), q=True, t=True, ws=True),name="Rig_L_Leg_2")
        L_upperLegJoint3 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('Loc_LeftLeg_3', type='transform'), q=True, t=True, ws=True),name="Rig_L_Leg_3")
        L_upperLegJoint4 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('Loc_LeftLeg_4', type='transform'), q=True, t=True, ws=True),name="Rig_L_Leg_4")

        # mirror joint
        cmds.mirrorJoint('Rig_L_UpperArm0',mirrorYZ=True,searchReplace=('L_', 'R_'))
        cmds.mirrorJoint('Rig_L_Leg_0',mirrorYZ=True,searchReplace=('L_', 'R_'))
        # create quadra ped
    else:
        # left frontLeg
        L_backLegJoint = cmds.joint(radius=1,p=cmds.xform(cmds.ls('R_Leg_Back_0', type='transform'), q=True, t=True, ws=True),name="Rig_L_BackLeg_0")
        L_backLegJoint1 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('R_Leg_Back_1', type='transform'), q=True, t=True, ws=True),name="Rig_L_BackLeg_1")
        L_backLegJoint2 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('R_Leg_Back_2', type='transform'), q=True, t=True, ws=True),name="Rig_L_BackLeg_2")

        # left frontLeg
        cmds.select(d=True)
        cmds.select('Rig_Spine_0')

        L_frontLegJoint = cmds.joint(radius=1,p=cmds.xform(cmds.ls('R_Leg_front_0', type='transform'), q=True, t=True, ws=True),name="Rig_L_FrontLeg_0")
        L_frontLegJoint1 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('R_Leg_front_1', type='transform'), q=True, t=True, ws=True),name="Rig_L_FrontLeg_1")
        L_frontLegJoint2 = cmds.joint(radius=1,p=cmds.xform(cmds.ls('R_Leg_front_2', type='transform'), q=True, t=True, ws=True),name="Rig_L_FrontLeg_2")

        # mirror joint
        cmds.mirrorJoint('Rig_L_BackLeg_0', mirrorYZ=True, searchReplace=('L_', 'R_'))
        cmds.mirrorJoint('Rig_L_FrontLeg_0', mirrorYZ=True, searchReplace=('L_', 'R_'))

    createHead(len(allSpine))
    if rig_Type==1:
        createFingerLoop()
    else:
        createTail()

def createFingerLoop():
    for x in range(0,4):
        createFingerJoints(x)

def createFingerJoints(i):
    if rig_Type ==1:
        cmds.select(deselect =True)
        cmds.select("Rig_L_UpperArm2")
        l_allFingers =cmds.ls("Loc_L_Finger_"+str(i)+"_*",type ='transform')
        l_fingers =cmds.listRelatives(l_allFingers,p=True,s=False)

        for x,f in enumerate(l_allFingers):
            l_pos =cmds.xform(f,q=True,t=True,ws=True)
            l_j=cmds.joint(radius=1,p=l_pos,name="RIG_L_Finger_"+str(i)+"_"+str(x))

        cmds.select(deselect=True)
        cmds.select("Rig_R_UpperArm2")
        r_allFingers = cmds.ls("Loc_R_Finger_" + str(i) + "_*", type='transform')
        r_fingers = cmds.listRelatives(r_allFingers, p=True, s=False)

        for y, g in enumerate(r_allFingers):
            r_pos = cmds.xform(g, q=True, t=True, ws=True)
            r_j = cmds.joint(radius=1, p=r_pos, name="RIG_L_Finger_" + str(i) + "_" + str(y))

def createHead(count):
    cmds.select(deselect =True)
    cmds.select("Rig_Spine_"+str(count-1))

    neckJoint= cmds.joint(radius=1,p=cmds.xform(cmds.ls('Loc_Neck_0'),q=True,t=True,ws=True),name="RIG_Neck_0")
    cmds.joint(radius=1, p=cmds.xform(cmds.ls('Loc_Neck_1'), q=True, t=True, ws=True), name="RIG_Neck_1")
    cmds.joint(radius=1, p=cmds.xform(cmds.ls('Loc_Neck_2'), q=True, t=True, ws=True), name="RIG_Neck_2")

def createTail():
    cmds.select(deselect =True)
    cmds.select("Rig_Spine_0")

    start=cmds.ls("Loc_Spine_0")

    allTail = cmds.ls("Loc_Tail_*", type='locator')
    tail = cmds.listRelatives(*allTail, p=True, f=True)
    rootPos = cmds.xform(start, q=True, t=True, ws=True)

    # create spine
    for i, j in enumerate(tail):
        pos = cmds.xform(j, q=True, t=True, ws=True)
        j = cmds.joint(radius=2, p=pos, name="Rig_Tail_"+ str(i))
