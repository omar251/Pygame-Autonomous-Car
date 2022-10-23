import math
# list = [[(10,10),1],[(20,20),2],[(30,30),3]]
# dist= [i[1] for i in list]
# emp = [1]
# emp.pop(0)
# print(list[dist.index(max(dist))][0])
# print(len(emp))

def ang(source,destination):
    speed = int(math.hypot(destination[0] - source[0],destination[1] - source[1]))           
    new_angle = int(math.degrees(math.atan2(-(destination[1] - source[1]), destination[0] - source[0])))
    radians = math.radians(new_angle)
    dx = int(math.cos(radians)*speed)
    dy = int(math.sin(radians)*speed)
    angle_of_rotation = (new_angle)
    return angle_of_rotation,dx,dy
angle_of_rotation,dx,dy = ang((0,0),(0,-1))

print(angle_of_rotation,int(abs(abs(angle_of_rotation) - 180) * -(abs(angle_of_rotation)/angle_of_rotation)),dx,dy)
# print((abs(1)/-1))
if abs(angle_of_rotation) > abs(abs(angle_of_rotation) - 180):
    angle_of_rotation = int(abs(abs(angle_of_rotation) - 180) * -(abs(angle_of_rotation)/angle_of_rotation))

if 0 <= angle_of_rotation <= 90 or -270 > angle_of_rotation >= -360:
    print(1,angle_of_rotation)
elif 90 < angle_of_rotation <= 180 or -180 > angle_of_rotation >= -270:
    print(2,angle_of_rotation)          
elif 180 < angle_of_rotation <= 270 or -90 > angle_of_rotation >= -180:
    print(3,angle_of_rotation)
elif 270 < angle_of_rotation <= 360 or 0 >= angle_of_rotation >= -90:
    print(4,angle_of_rotation)
# elif 0 >= angle_of_rotation >= -90:
#     print(4,angle_of_rotation)
# elif -90 > angle_of_rotation >= -180:
#     print(3,angle_of_rotation)          
# elif -180 > angle_of_rotation >= -270:
#     print(2,angle_of_rotation)
# elif -270 > angle_of_rotation >= -360:
#     print(1,angle_of_rotation)