BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "twitch" (
	"ID"	INTEGER,
	"Query"	TEXT NOT NULL,
	"StreamerLink"	TEXT NOT NULL,
	"StartStream"	TEXT,
	PRIMARY KEY("id")
);
INSERT OR REPLACE INTO "twitch" ("ID","Query","StreamerLink","StartStream") VALUES (14371185,'northernlion','https://www.twitch.tv/northernlion',NULL);
INSERT OR REPLACE INTO "twitch" ("ID","Query","StreamerLink","StartStream") VALUES (22510310,'gamesdonequick','https://www.twitch.tv/gamesdonequick', NULL);
INSERT OR REPLACE INTO "twitch" ("ID","Query","StreamerLink","StartStream") VALUES (35958947,'squeex','https://www.twitch.tv/squeex',NULL);
INSERT OR REPLACE INTO "twitch" ("ID","Query","StreamerLink","StartStream") VALUES (37650924,'chiblee','https://www.twitch.tv/chiblee',NULL);
COMMIT;
