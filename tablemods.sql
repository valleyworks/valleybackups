ALTER TABLE "Job" ADD COLUMN "archive" INTEGER DEFAULT 0 NOT NULL REFERENCES "Archive" ("id");
