import maya.cmds as cmds

def globalNames(): 
	global spineCount
    
    cmds.text("Spine Count",l="Spine Count:",align ="center")
    spineCount = cmds.intField(minValue=1, maxValue=10, value=4)

def generateLocators(*args):
    if cmds.objExists("LOC_Master"):
        print 'Joints Master already exists.'
    else:
        cmds.group(em =True,name ='LOC_Master')
    root  = cmds.spaceLocator(n = "LOC_ROOT")
    cmds.scale(0.5,0.5,0.5,root)
    cmds.move(0,1,0,root)
    cmds.parent (root,"LOC_Master")
    createSpine()

def createSpine():
    #rig_Type = cmds.optionMenu('rig_Menu_Type', q=True, sl=True)
    globalNames()
    
    for i in range(0, cmds.intField(spineCount, q=True, value =True)):
        spine = cmds.spaceLocator(n='Loc_SPINE_'+ str(i))
        cmds.move(0, (4*i), 0, spine)
        #cmds.parent(spine,'LOC_ROOT')

        if i==0:
            cmds.parent (spine,'LOC_ROOT')
        else:
            cmds.parent(spine, 'Loc_SPINE_'+str(i-1))

    if rig_Type ==1:
        cmds.move(0,20,0,'LOC_Master')
    if rig_Type ==2:
        cmds.rotate(90, 0, 0, 'LOC_Master')
        cmds.move(0, 10, -2, 'LOC_Master')

    createArms(1)
    createArms(-1)
    createLegs(1)
    createLegs(-1)

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
                for i in range (0,3):
                    upperArm= cmds.spaceLocator (n='Loc_LeftArm_'+str(i))
                    cmds.move((8 * i),0 , 0, upperArm, preserveChildPosition=False)

                    if i ==0:
                        cmds.parent (upperArm,L_arm)
                    else:
                        cmds.parent (upperArm,'Loc_LeftArm_'+str(i-1))

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
                for i in range (0,3):
                    upperArm= cmds.spaceLocator(n='Loc_RightArm_'+str(i))
                    cmds.move((-8 * i),0 , 0, upperArm)

                    if i ==0:
                        cmds.parent(upperArm,R_arm)
                    else:
                        cmds.parent(upperArm, 'Loc_RightArm_' + str(i - 1))
                tempConst=cmds.parentConstraint(R_arm,'Loc_RightArm_'+str(0),mo=False)
                cmds.delete(tempConst)
    else:
        if side == 1:  # for Left_Leg
            if cmds.objExists("L_Leg_Front_GRP"):
                print "is not doing anything"
            else:
                L_leg_front = cmds.group(em=True, name='L_Leg_Front_GRP')
                cmds.parent(L_leg_front, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2 * side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), -3, L_leg_front,r=1)

                #Create the locators left leg
                for i in range (0,3):
                    front_Locator= cmds.spaceLocator(n='L_Leg_front_'+str(i))
                    cmds.move(2 ,(2 * i), -2, front_Locator) #(5 * i)

                    if i ==0:
                        cmds.parent(front_Locator,L_leg_front)
                    else:
                        cmds.parent(front_Locator, 'L_Leg_front_' + str(i - 1))

                    tempConst = cmds.parentConstraint(L_leg_front, 'L_Leg_front_' + str(0), mo=False)
                    cmds.delete(tempConst)

        else:  # for Right_leg
            if cmds.objExists('R_Leg_Front_GRP'):
                print "is not doing anything"
            else:
                R_leg_front = cmds.group(em=True, name='R_Leg_Front_GRP')
                cmds.parent(R_leg_front, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2* side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), -3, R_leg_front,r=1)

                # Create the locators right leg
                for i in range(0, 3):
                    front_Locator = cmds.spaceLocator(n='R_Leg_front_' + str(i))
                    cmds.move(-2 ,(2 * i), -2, front_Locator)

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
                for i in range (0,3):
                    upperLeg= cmds.spaceLocator (n='Loc_LeftLeg_'+str(i))
                    cmds.move(0 ,(-8.5 * i), 0, upperLeg, preserveChildPosition=False)

                    if i ==0:
                        cmds.parent (upperLeg,L_leg)
                    else:
                        cmds.parent (upperLeg,'Loc_LeftLeg_'+str(i-1))

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
                for i in range (0,3):
                    upperLeg= cmds.spaceLocator(n='Loc_RightLeg_'+str(i))
                    cmds.move(0 ,(-8.5 * i), 0, upperLeg)
                    if i ==0:
                        cmds.parent(upperLeg,R_leg)
                    else:
                        cmds.parent(upperLeg, 'Loc_RightLeg_' + str(i - 1))
                tempConst=cmds.parentConstraint(R_leg,'Loc_RightLeg_'+str(0),mo=False)
                cmds.delete(tempConst)
    else:
        if side == 1:  # for Left_Leg_Back
            if cmds.objExists("L_Leg_Back_GRP"):
                print "is not doing anything"
            else:
                L_leg_back = cmds.group(em=True, name='L_Leg_Back_GRP')
                cmds.parent(L_leg_back, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2 * side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), 11, L_leg_back,r=1)

                #Create the locators left leg
                for i in range (0,3):
                    back_Locator= cmds.spaceLocator(n='L_Leg_Back_'+str(i))
                    cmds.move(2 ,(2 * i), 11, back_Locator) #(5 * i)

                    if i ==0:
                        cmds.parent(back_Locator,L_leg_back)
                    else:
                        cmds.parent(back_Locator, 'L_Leg_Back_' + str(i - 1))

                    tempConst = cmds.parentConstraint(L_leg_back, 'L_Leg_Back_' + str(0), mo=False)
                    cmds.delete(tempConst)

        else:  # for Right_leg_Back
            if cmds.objExists('R_Leg_Back_GRP'):
                print "is not doing anything"
            else:
                R_leg_back = cmds.group(em=True, name='R_Leg_Back_GRP')
                cmds.parent(R_leg_back, 'Loc_SPINE_' + str(cmds.intField(spineCount, query=True, value=True) - 1))
                cmds.move(2* side, 1 + (2 * cmds.intField(spineCount, query=True, value=True)), 11, R_leg_back,r=1)

                # Create the locators right leg
                for i in range(0, 3):
                    back_Locator = cmds.spaceLocator(n='R_Leg_Back_' + str(i))
                    cmds.move(-2 ,(2 * i), 11, back_Locator)

                    if i == 0:
                        cmds.parent(back_Locator, R_leg_back)
                    else:
                        cmds.parent(back_Locator, 'R_Leg_Back_' + str(i - 1))

                    tempConst = cmds.parentConstraint(R_leg_back, 'R_Leg_Back_' + str(0), mo=False)
                    cmds.delete(tempConst)