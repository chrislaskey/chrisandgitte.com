CREATE TABLE IF NOT EXISTS "main"."rsvps" (
	 "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	 "attending" text NOT NULL,
	 "name" text NOT NULL,
	 "guests" text NOT NULL,
	 "allergies" text NOT NULL,
	 "comments" text NOT NULL,
	 "date" text NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "main"."rsvp_id" ON "rsvps" (id);
