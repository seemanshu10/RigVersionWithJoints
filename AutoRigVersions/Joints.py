import maya.cmds as cmds
import Locators

Locators =reload(Locators)

def CreateJointsWindow():
	cmds.button(l='Create Joints ', c="Joints.createJoints()")
	
def createJoints(*args):
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

    createHead(spineCount)

def createHead(count):
    cmds.select(deselect =True)
    cmds.select("Rig_Spine_"+str(count-1))

    neckJoint= cmds.joint(radius=1,p=cmds.xform(cmds.ls('Loc_Neck_0'),q=True,t=True,ws=True),name="RIG_Neck_0")
    cmds.joint(radius=1, p=cmds.xform(cmds.ls('Loc_Neck_1'), q=True, t=True, ws=True), name="RIG_Neck_1")
    cmds.joint(radius=1, p=cmds.xform(cmds.ls('Loc_Neck_2'), q=True, t=True, ws=True), name="RIG_Neck_2")

