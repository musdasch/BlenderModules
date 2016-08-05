from bge import constraints, events, logic, render, types
from mathutils import Vector

class MouseLook:
    
    def __init__( self, cont ):
        
        self.cont = cont
        self.owner = cont.owner
        self.cam = self.owner.children[0]
        
        self.sen_mous = self.cont.sensors[ "Mouse" ]
        
        x = render.getWindowWidth()//2
        y = render.getWindowHeight()//2
        self.screen_center = ( x, y )
        
        render.setMousePosition( * self.screen_center )
    
    def getMouseOffset( self ):
        
        vec_screencenter = Vector( self.screen_center )
        vec_mouseposition = Vector( self.sen_mous.position )
        
        return vec_mouseposition - vec_screencenter
    
    def main( self ):
        
        vec_offset = self.getMouseOffset()
        vec_offset *= -0.0005
        
        cam_rotation = self.cam.localOrientation.to_euler()
        own_rotation = self.owner.worldOrientation.to_euler()
        
        if cam_rotation.x + vec_offset.y > 0 and cam_rotation.x + vec_offset.y < 3:
            cam_rotation.x += vec_offset.y
            
        own_rotation.z += vec_offset.x
        
        self.cam.localOrientation = cam_rotation
        self.owner.worldOrientation = own_rotation
        
        
        render.setMousePosition( * self.screen_center )

class Key:
    
    def active( self, key_code ):
        
        if logic.keyboard.events[ key_code ] == logic.KX_INPUT_ACTIVE:
            return True
        return False
    

class KeyMotion:
    
    def __init__( self, cont ):
        
        self.cont = cont
        self.owner = cont.owner
        
        self.wrapper = constraints.getCharacter( self.cont.owner )
        
        self.keyActive = Key()
        
        self.walkSpeed = 0.3
        self.runSpeed = 0.3
        self.jumpHeight = 1
    
    
    def main( self ):
        
        up_down = self.keyActive.active( events.SKEY ) - self.keyActive.active( events.WKEY )
        right_left = self.keyActive.active( events.DKEY ) - self.keyActive.active( events.AKEY )
        jump = self.keyActive.active( events.SPACEKEY ) * self.jumpHeight
        
        delta = Vector( ( up_down, right_left, 0 ) )
        delta *= self.walkSpeed + ( self.keyActive.active( events.LEFTCTRLKEY ) * self.runSpeed )
        
        if jump:
            self.wrapper.jump()
        
        
        self.owner.applyMovement( delta, True )
        

     
class Avatar:
    
    def __init__( self, cont ):
        
        self.init = False
        self.mouseLook = MouseLook( cont )
        self.keyMotion = KeyMotion( cont )
    
    def main( self ):
        
        if self.init:
            self.mouseLook.main()
            self.keyMotion.main()
        else:
            self.init = True


avatar = Avatar( logic.getCurrentController() )

def main():
    avatar.main()
