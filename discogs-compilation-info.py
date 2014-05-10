import sys
import discogs_client as discogs

if (len(sys.argv) != 2):
	print "Usage: discogs-compilation-info.py release-id";
	print "(release-id is the numeric id of the compilation you want to query about"
	exit(0)

discogs.user_agent = 'Discogs-Compilation-Info/0.1 +http://github.com/marado/discogs-compilation-info'
compilation = discogs.Release(sys.argv[1])
tracklist = compilation.tracklist
for t in tracklist:
	artists = ""
  	for a in  t['artists']:
		artists += a.data['name']
	print artists + ": " + t['title']
