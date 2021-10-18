CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry text` TEXT NOT NULL,
    `entry date` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Moods` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `mood_type` TEXT NOT NULL
);

INSERT INTO `ENTRIES` VALUES (null, 'Confused', 'Feeling pretty confused on my processes with SQL.', '20211015', 3);
INSERT INTO `ENTRIES` VALUES (null, 'Optomistic', 'I am optomistic that I will understand SQL and its innner workings.', '20211018', 6);
INSERT INTO `ENTRIES` VALUES (null, 'Proud', 'Today I am proud that i have decided to make a career change', '202110117', 5);

INSERT INTO `Moods` VALUES (null, 'Happy');
INSERT INTO `Moods` VALUES (null, 'Angry');
INSERT INTO `Moods` VALUES (null, 'Confused');
INSERT INTO `Moods` VALUES (null, 'Bleak');
INSERT INTO `Moods` VALUES (null, 'Proud');
INSERT INTO `Moods` VALUES (null, 'Optomistic');

