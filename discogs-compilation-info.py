import sys
import discogs_client as discogs
import time

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
		time.sleep(1) # because discogs_client doesn't do this for us
	print artists + ": " + t['title']
	# for now, we'll only look for info on tracks with only one artist
	if (len(t['artists']) == 1):
		artist = t['artists'][0]
		print ":: This artist has the following albums: "
		for rel in artist.releases:
			time.sleep(1) # because discogs_client doesn't do this for us
			if rel.__class__.__name__ == 'MasterRelease':
				# TODO: deal with master releases (they don't have format...)
				next
			if rel.data.has_key('formats'):
				for formt in rel.data['formats']:
					for formtitem in formt:
						if formtitem == 'descriptions':
							for desc in formt[formtitem]:
								if desc == 'Album' or desc == 'MiniAlbum':
									try:
										if len(rel.artists) == 1 and rel.artists[0].data['name'] == artist.data['name']:
											print ":: : " + rel.data['title'] + " (" + desc + ")"
										else:
											print "DEBUG: excluding one album because it isn't from the artist we're looking at: " + rel.data['title']
									except DiscogsAPIError as e: # this needs the git version of discogs-client, which fixes a bug in exceptions usage
										if e == "200 OK":
											#TODO: we should retry
											print "We should be retrying a call but we aren't!"
										else:
											print "Oops, we've got a DiscogsAPIError: " + e
