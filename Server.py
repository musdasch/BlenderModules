from bge import logic
import socket
import pickle

class RemoteKeyboard:
    
    def __init__( self ):
        
        self.key_stat = {}
    
    def updateState( self , list_key_stat ):
        
        for key, state in list_key_stat:
            self.key_stat[ key ] = state
            
    def keyDown( self , key_code, status=logic.KX_INPUT_ACTIVE ):
        
        if key_code in self.key_stat:
            if self.key_stat[ key_code ] == status:
                return True
            
        return False
    
class User:
    
    def __init__( self, name ):
        
        self.name = name
        self.keyboard = RemoteKeyboard()
    
class Server:
    
    def __init__( self, host="localhost", port=9999 ):
        
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socket.setblocking( False )
        self.socket.bind( ( host, port ) )
        
        self.user_addr = {}
    
    def receive( self ):
        
        while True:
            try:
                data, addr = self.socket.recvfrom( 1024 )
                
                if not addr in self.user_addr:
                    user = User( data.decode() )
                    
                    scene = logic.getCurrentScene()
                    spawner = scene.objects[ "Spawner" ]
                    avatar = scene.addObject( "Avatar", spawner )
                    avatar.children[ 0 ]["Text"] = user.name
                    avatar[ "user" ] = user
                    
                    self.user_addr[ addr ] = user
                    
                else:
                    user = self.user_addr[ addr ]
                    user.keyboard.updateState( pickle.loads( data ) )
                     
            except socket.error:
                break
            
    def send( self ):
        
        scene = logic.getCurrentScene()
        
        state = { ( gobj.name, gobj[ "user" ].name ): list( gobj.worldPosition ) \
                    for gobj in scene.objects \
                    if gobj.name == "Avatar" }
        
        for addr in self.user_addr:
            self.socket.sendto( pickle.dumps( state ), addr )
            
    
    def end( self ):
        self.socket.close()

server = Server()

def receive():
    server.receive()

def send():
    server.send()
    
def end():
    server.end()
    logic.endGame()
