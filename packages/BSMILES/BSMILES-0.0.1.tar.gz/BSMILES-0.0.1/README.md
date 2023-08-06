# transformation between smiles and bsmiles
All chemical molecules can be represented by SMILES notation. But from SMILES notation, can not seperate molecules into fragments directly. Here I create a new notation called BSMILES which is easier to check each fragment.

Example:

  SMILES notation: O(=C1CSC(c4ccccn4)N(c2ccc3c(cccc3)c2)1)   
  
  BSMILES notation: O{0=C!CSCN!{4c%ccc!c(cccc!)c%}{3c!ccccn!}}
  
  ## how to convert SMILES to BSMILES
    from BSMILES.BSMILES import encode 

     bsmiles = encode(smiles)

  ## how to convert BSMILES back to SMILES
    from BSMILES.B_to_smiles import convertB 

    smiles = convertB(bsmiles)

  ## how to get fragments from BSMILES notation
  1. input one file then got one output file
    from BSMILES.B_to_smiles import bsmiles_to_frag 

    inputfile_name ="bsmiles"
    outputfile_name="fragment"
    bsmiles_to_frag(inputfile_name,outputfile_name)

  2. input one bsmiles string return two vectors, the second one contains fragments.
    from BSMILES.B_to_smiles import getFragments
    
    bsmiles = "any_kind_of_bsmiles"
    visited = []#contain all unique fragments from bsmiles
    fragments = []#contain all fragments
    visited,bsmiles = getFragments(visited,bsmiles)
