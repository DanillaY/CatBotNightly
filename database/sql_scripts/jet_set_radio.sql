BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "jet_set_radio" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"SongName"	TEXT NOT NULL,
	"SongLink"	TEXT NOT NULL UNIQUE,
	"Station"	TEXT NOT NULL,
	"GameTitle"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (1,'Yappie Feet','https://jetsetradio.live/radio/stations/classic/Deavid%20Soul%20-%20Yappie%20Feet.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (2,'Funky Radio','https://jetsetradio.live/radio/stations/classic/B.B.%20Rights%20-%20Funky%20Radio.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (3,'Mischievous Boy','https://jetsetradio.live/radio/stations/classic/Castle%20Logical%20-%20Mischievous%20Boy.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (4,'Dunny Boy Williamson Show','https://jetsetradio.live/radio/stations/classic/Deavid%20Soul%20-%20Dunny%20Boy%20Williamson%20Show.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (5,'Miller Ball Breakers','https://jetsetradio.live/radio/stations/classic/Deavid%20Soul%20-%20Miller%20Ball%20Breakers.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (6,'On The Bowl (A. Fargus Mix)','https://jetsetradio.live/radio/stations/classic/Deavid%20Soul%20-%20On%20The%20Bowl%20(A.%20Fargus%20Mix).mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (7,'Up-Set Attack','https://jetsetradio.live/radio/stations/classic/Deavid%20Soul%20-%20Up-Set%20Attack.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (8,'Yellow Bream','https://jetsetradio.live/radio/stations/classic/F-Fields%20-%20Yellow%20Bream.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (9,'Recipe For The Perfect Afro','https://jetsetradio.live/radio/stations/classic/Featurecast%20-%20Recipe%20For%20The%20Perfect%20Afro.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (10,'Magical Girl','https://jetsetradio.live/radio/stations/classic/Guitar%20Vader%20-%20Magical%20Girl.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (11,'Super Brothers','https://jetsetradio.live/radio/stations/classic/Guitar%20Vader%20-%20Super%20Brothers.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (12,'Grace & Glory','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Grace%20&%20Glory.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (13,'Humming The Bassline','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Humming%20The%20Bassline.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (14,'Jet Set Medley','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Jet%20Set%20Medley.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (15,'Let Mom Sleep','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Let%20Mom%20Sleep.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (16,'Moody''s Shuffle','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Moody''s%20Shuffle.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (17,'Rock It On','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Rock%20It%20On.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (18,'Sneakman','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Sneakman.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (19,'Sweet Soul Brother','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20Sweet%20Soul%20Brother.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (20,'That''s Enough','https://jetsetradio.live/radio/stations/classic/Hideki%20Naganuma%20-%20That''s%20Enough.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (21,'O.K. House','https://jetsetradio.live/radio/stations/classic/Idol%20Taxi%20-%20O.K.%20House.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (22,'Improvise','https://jetsetradio.live/radio/stations/classic/Jurassic%205%20-%20Improvise.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (23,'Patrol Knob','https://jetsetradio.live/radio/stations/classic/Mix%20Master%20Mike%20-%20Patrol%20Knob.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (24,'Bout The City','https://jetsetradio.live/radio/stations/classic/Reps%20-%20Bout%20The%20City.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (25,'Everybody Jump Around','https://jetsetradio.live/radio/stations/classic/Richard%20Jacques%20-%20Everybody%20Jump%20Around.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (26,'Electric Tooth Brush','https://jetsetradio.live/radio/stations/classic/Toronto%20-%20Electric%20Tooth%20Brush.mp3','Classic','Jet Set Radio');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (27,'Statement of Intent (Remix)','https://jetsetradio.live/radio/stations/future/bis%20-%20Statement%20of%20Intent%20(Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (28,'The Answer (The Latch Brothers Remix)','https://jetsetradio.live/radio/stations/future/Bran%20Van%203000%20-%20The%20Answer%20(The%20Latch%20Brothers%20Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (29,'The Scrappy (The Latch Brothers Remix)','https://jetsetradio.live/radio/stations/future/BS%202000%20-%20The%20Scrappy%20(The%20Latch%20Brothers%20Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (30,'Birthday Cake','https://jetsetradio.live/radio/stations/future/Cibo%20Matto%20-%20Birthday%20Cake.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (31,'Baby-T','https://jetsetradio.live/radio/stations/future/Guitar%20Vader%20-%20Baby-T.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (32,'I Love Love You (Love Love Super Dimension Mix)','https://jetsetradio.live/radio/stations/future/Guitar%20Vader%20-%20I%20Love%20Love%20You%20(Love%20Love%20Super%20Dimension%20Mix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (33,'Fly Like a Butterfly','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Fly%20Like%20a%20Butterfly.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (34,'Funky Dealer','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Funky%20Dealer.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (35,'Grace & Glory (B.B. M.H. Mix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Grace%20&%20Glory%20(B.B.%20M.H.%20Mix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (36,'Humming the Bassline (D.S. Remix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Humming%20the%20Bassline%20(D.S.%20Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (37,'Jet Set Medley Future','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Jet%20Set%20Medley%20Future.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (38,'Let Mom Sleep (No Sleep Remix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Let%20Mom%20Sleep%20(No%20Sleep%20Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (39,'Like It Like This Like That','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Like%20It%20Like%20This%20Like%20That.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (40,'Oldies But Happies','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Oldies%20But%20Happies.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (41,'Rock It On (D.S. Remix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Rock%20It%20On%20(D.S.%20Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (42,'Shape Da Future','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Shape%20Da%20Future.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (43,'Sneakman (Toronto Mix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Sneakman%20(Toronto%20Mix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (44,'Sweet Soul Brother (B.B. Rights Mix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Sweet%20Soul%20Brother%20(B.B.%20Rights%20Mix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (45,'Teknopathetic','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20Teknopathetic.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (46,'That''s Enough (B.B. Rights Mix)','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20That''s%20Enough%20(B.B.%20Rights%20Mix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (47,'The Concept of Love','https://jetsetradio.live/radio/stations/future/Hideki%20Naganuma%20-%20The%20Concept%20of%20Love.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (48,'Bokfresh','https://jetsetradio.live/radio/stations/future/Richard%20Jacques%20-%20Bokfresh.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (49,'What About the Future','https://jetsetradio.live/radio/stations/future/Richard%20Jacques%20-%20What%20About%20the%20Future.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (50,'Aisle 10 (Hello Allison)','https://jetsetradio.live/radio/stations/future/Scapegoat%20Wax%20-%20Aisle%2010%20(Hello%20Allison).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (51,'Count Latchula','https://jetsetradio.live/radio/stations/future/The%20Latch%20Brothers%20-%20Count%20Latchula.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (52,'Ill Victory Beat','https://jetsetradio.live/radio/stations/future/The%20Latch%20Brothers%20-%20Ill%20Victory%20Beat.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (53,'Koto Stomp','https://jetsetradio.live/radio/stations/future/The%20Latch%20Brothers%20-%20Koto%20Stomp.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (54,'Latch Brother Bounce','https://jetsetradio.live/radio/stations/future/The%20Latch%20Brothers%20-%20Latch%20Brother%20Bounce.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (55,'Me Likey the Poom Poom','https://jetsetradio.live/radio/stations/future/The%20Latch%20Brothers%20-%20Me%20Likey%20the%20Poom%20Poom.mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (56,'Rockin'' the Mic (The Latch Brothers Remix)','https://jetsetradio.live/radio/stations/future/The%20Prunes%20-%20Rockin''%20the%20Mic%20(The%20Latch%20Brothers%20Remix).mp3','Future','Jet Set Radio Future');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (57,'Ain''t Nothin'' like A Funky Beat','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Ain''t%20Nothin''%20like%20A%20Funky%20Beat.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (58,'Beverly Chills','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Beverly%20Chills.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (59,'Decible','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Decible.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (60,'Dial Hop','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Dial%20Hop.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (61,'Dominator','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Dominator.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (62,'Headbangeren','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Headbangeren.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (63,'Jungaaaa','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Jungaaaa.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (64,'Killa Swing','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Killa%20Swing.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (65,'Nasty Lovers','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Nasty%20Lovers.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (66,'Ordinary Days V1','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Ordinary%20Days%20V1.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (67,'Ordinary Days V2','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Ordinary%20Days%20V2.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (68,'Ruiner','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Ruiner.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (69,'Scream','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Scream.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (70,'Shred','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Shred.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (71,'Snibbit','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Snibbit.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (72,'Thuggin','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Thuggin.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (73,'Urabon','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Urabon.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (74,'Whipz','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20Whipz.mp3','Lethalleagueblaze','Lethal league blaze');
INSERT OR REPLACE INTO "jet_set_radio" ("ID","SongName","SongLink","Station","GameTitle") VALUES (75,'X','https://jetsetradio.live/radio/stations/lethalleagueblaze/Lethal%20League%20Blaze%20-%20X.mp3','Lethalleagueblaze','Lethal league blaze');
COMMIT;
