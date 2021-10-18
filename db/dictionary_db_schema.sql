CREATE SCHEMA IF NOT EXISTS dictionary;

CREATE TABLE IF NOT EXISTS dictionary.words(
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(64) NOT NULL,
    language VARCHAR(32) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_words_word ON dictionary.words(word, language);

CREATE TABLE IF NOT EXISTS dictionary.synonyms(
    id INT AUTO_INCREMENT PRIMARY KEY,
    word_id INT NOT NULL,
    synonym_id INT NOT NULL,
    UNIQUE (word_id, synonym_id),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_synonyms_word_id ON dictionary.synonyms(word_id);

CREATE TABLE IF NOT EXISTS dictionary.word_types(
    id INT AUTO_INCREMENT PRIMARY KEY,
    word_id INT NOT NULL,
    name VARCHAR(32) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_word_types_word_id ON dictionary.word_types(word_id);
