'''
    Create new zip files that contain only particles above a certain size

'''

try:
    import planktonator as plktor
except:
    from context import planktonator as plktor
import os

cruise  = 'DY090'
event   = 154
project = 'ecotaxa_' + cruise + '_event' + str(event)
majthresh   = 40

# zip file path
# zipfile     = "".join(('../img/',project,'.zip')) 
zipfile     = "".join(('J:/',cruise,'/LISST-HOLO/reconstructed/event_',str(event),'/',project,'.zip'))

# extraction path
# extractpath = "".join(('../img/',project,'_tmp'))
extractpath     = "".join(('J:/',cruise,'/LISST-HOLO/reconstructed/event_',str(event),'/' , project, '_tmp'))

# unzip ecotaxa file
plktor.tools.zipextract(extractpath,zipfile)

# Load .tsv file 
ecotax      = plktor.metadata.EcoTaxa()
ecotax.loadtsv(os.path.join(extractpath,project + '.tsv'))


# find all indices with object major above threshold
ecotax.subset(header='object_major',val=majthresh)

# remove files not in list 
for f in os.listdir(extractpath):
    if not ecotax.df['img_file_name'].str.contains(f).any():
        os.remove(os.path.join(extractpath,f))

# save 
ecotax.save(os.path.join(extractpath,project + '_subset.tsv'))

# Create new zip file of data
plktor.tools.zipcompress(extractpath,zipf="".join(('J:/',cruise,'/LISST-HOLO/reconstructed/event_',str(event),'/',project + '_subset')))

# delete tmp 
plktor.tools.rmfolder(extractpath)