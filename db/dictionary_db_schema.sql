CREATE SCHEMA IF NOT EXISTS dictionary;

CREATE TABLE IF NOT EXISTS dictionary.words(
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(64) NOT NULL,
    language VARCHAR(32) NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_words_word ON dictionary.words(word, language);

CREATE TABLE IF NOT EXISTS dictionary.synonyms(
    id INT AUTO_INCREMENT PRIMARY KEY,
    word_id INT NOT NULL,
    synonym_id INT NOT NULL,
    meaning_group INT NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (word_id, synonym_id, meaning_group),
    FOREIGN KEY (word_id) REFERENCES dictionary.synonyms(id) ON DELETE CASCADE,
    FOREIGN KEY (synonym_id) REFERENCES dictionary.synonyms(id) ON DELETE CASCADE
);

CREATE INDEX idx_synonyms_word_id ON dictionary.synonyms(word_id);

CREATE TABLE IF NOT EXISTS dictionary.word_types(
    id INT AUTO_INCREMENT PRIMARY KEY,
    synonym_id INT NOT NULL,
    type VARCHAR(32) NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (synonym_id) REFERENCES dictionary.synonyms(id) ON DELETE CASCADE
);

CREATE INDEX idx_word_types_word_id ON dictionary.word_types(synonym_id);
