from bge import logic, types, events
from mathutils import Vector

class Avatar( types.KX_GameObject ):
    
    def __init__( self, own ):
        self.speed = 0.1
        self.user = self[ "user" ]
        
    def main( self ):
        
        k = self.user.keyboard.keyDown
        
        up_down = k( events.UPARROWKEY ) - k( events.DOWNARROWKEY )
        right_left = k( events.RIGHTARROWKEY ) - k( events.LEFTARROWKEY )
        
        delta = Vector( ( right_left, up_down, 0 ) )
        delta.magnitude = self.speed
        
        self.worldPosition += delta


cont = logic.getCurrentController()
avatar = Avatar( cont.owner )

def main():
    avatar.main()
