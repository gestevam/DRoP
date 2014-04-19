import scitbx.matrix
import ccp4io_adaptbx

UNIT = scitbx.matrix.rt( ( ( 1, 0, 0, 0, 1, 0, 0, 0, 1 ), ( 0, 0, 0 ) ) )
CACHE = {}

class Superposition(object):
    """
    Superposition data
    """
    
    def __init__(self, reference, moving, transformation, rmsd):
        
        self.reference = reference
        self.moving = moving
        self.transformation = transformation
        self.rmsd = rmsd
        
        
    def inverse(self):
        
        return self.__class__(
            reference = self.moving,
            moving = self.reference,
            transformation = self.transformation.inverse(),
            rmsd = self.rmsd
            )
    
    
def superpose(reference, moving, output): 
    
    #output.verbose( msg = "Superposition:" )
    #output.indent()
    #output.verbose( msg = "Reference: %s" % reference )
    #output.verbose( msg = "Moving: %s" % moving )
    #output.dedent()
    #output.verbose( msg = "" )
    
    if reference.composition.overlap( other = moving.composition ).empty():
        raise ValueError, "No overlap between ensembles"
    
    if reference == moving:
        #output.verbose( msg = "Identical molecules" )
        superposition = Superposition(
            reference = reference,
            moving = moving,
            transformation = UNIT,
            rmsd = 0.0
            )
        
    elif ( reference, moving ) in CACHE:
        #output.verbose( msg = "Result found in cache" )
        superposition = CACHE[ ( reference, moving ) ]
    
    elif ( moving, reference ) in CACHE:
        #output.verbose( msg = "Result found in cache (inverted)" )
        superposition = CACHE[ ( moving, reference ) ].inverse()
        
    else:
        #output.verbose( msg = "Running SSM..." )
        print "Running SSM..."
        try:
            ssm = ccp4io_adaptbx.SecondaryStructureMatching(
                moving = moving.root(),
                reference = reference.root()
                )
            
        except RuntimeError, e:
            #output.verbose( msg = "SSM superposition failed: %s" % e )
	    print "SSM FAILED %s"%e
            raise RuntimeError, "SSM failure"
        
        tm = ssm.get_matrix() 
        superposition = Superposition(
            reference = reference,
            moving = moving,
            transformation = scitbx.matrix.rt(
                ( ( tm[0:3] + tm[4:7] + tm[8:11] ), ( tm[3], tm[7], tm[11] ) )
                ),
            rmsd = ssm.ssm.rmsd
            )
        CACHE[ ( reference, moving ) ] = superposition
        
    #output.verbose( msg = "Rmsd: %.3f" % superposition.rmsd )
    
    #output.verbose( msg = "Rotation: " )
    #output.indent()
    rotm = superposition.transformation.r.elems
    #output.verbose( msg = "%.4f %.4f %.4f" % rotm[0:3] )
    #output.verbose( msg = "%.4f %.4f %.4f" % rotm[3:6] )
    #output.verbose( msg = "%.4f %.4f %.4f" % rotm[6:9] )
    #output.dedent()
    #output.verbose(
    #    msg = "Translation: %.4f %.4f %.4f" % superposition.transformation.t.elems
    #    )
    
    return superposition


def substitue(peak, alternative, cell, output):
       
    output.verbose( msg = "Substituting ensemble in peak:" )
    output.indent()
    output.verbose( msg = str( speak ) )
    output.dedent()
    output.verbose( msg = "with ensemble: %s" % alternative )
    
    superposition = superpose(
        reference = peak.ensemble,
        moving = alternative,
        output = output
        )
    superposed = peak.as_scitbx_rt_operator( cell = cell ) * superposition.transformation
    substituted = mr_object.Peak(
        ensemble = alternative,
        rotation = mr_object.Rotation.Matrix( elements = superposed.r.elems ),
        translation = cell.fractionalize( superposed.t.elems ),
        bfactor = peak.bfactor
        )
    
    output.verbose( msg = "Substituted peak:" )
    output.indent()
    output.verbose( msg = str( substituted ) )
    output.dedent()
    
    return substituted


