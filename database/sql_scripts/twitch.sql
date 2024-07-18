BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "twitch" (
	"id"	INTEGER,
	"query"	TEXT NOT NULL,
	"streamer_link"	TEXT NOT NULL,
	"start_stream"	TEXT,
	PRIMARY KEY("id")
);
INSERT OR REPLACE INTO "twitch" ("id","query","streamer_link","start_stream") VALUES (14371185,'northernlion','https://www.twitch.tv/northernlion',NULL);
INSERT OR REPLACE INTO "twitch" ("id","query","streamer_link","start_stream") VALUES (22510310,'gamesdonequick','https://www.twitch.tv/gamesdonequick', NULL);
INSERT OR REPLACE INTO "twitch" ("id","query","streamer_link","start_stream") VALUES (35958947,'squeex','https://www.twitch.tv/squeex',NULL);
INSERT OR REPLACE INTO "twitch" ("id","query","streamer_link","start_stream") VALUES (37650924,'chiblee','https://www.twitch.tv/chiblee',NULL);
COMMIT;
