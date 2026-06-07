-- initial dataset: SQL database backup downloaded from
-- International Speculative Fiction Database (ISFDB).
-- backup dated from : 2026-06-06 
-- https://isfdb.org/wiki/index.php/ISFDB_Downloads (requires free account)
-- 

-- create table of novel simple details: titles, authors, pub date, isbn, publisher, synopsis, tags

SELECT titles.title_id as title_id,
    titles.title_title AS title,
    titles.title_ttype AS type,
    authors.author_canonical AS author,
    YEAR(MIN(pubs.pub_year)) AS first_publication_year,
    notes.note_note AS synopsis,
    title_tags.tags AS tags,
    (SELECT p2.pub_isbn 
     FROM pubs p2
     JOIN pub_content pc2 ON p2.pub_id = pc2.pub_id
     WHERE pc2.title_id = titles.title_id
     AND YEAR(p2.pub_year) > 0
     ORDER BY p2.pub_year ASC
     LIMIT 1) AS first_isbn,
    (SELECT pub3.publisher_name
        FROM pubs p3
        JOIN pub_content pc3 ON p3.pub_id = pc3.pub_id
        JOIN publishers pub3 ON p3.publisher_id = pub3.publisher_id
        WHERE pc3.title_id = titles.title_id
        AND p3.pub_year IS NOT NULL
        AND YEAR(p3.pub_year) > 0
        ORDER BY p3.pub_year ASC
        LIMIT 1) AS first_publisher,
    (SELECT i.identifier_value
        FROM identifiers i
        JOIN pub_content pc4 ON i.pub_id = pc4.pub_id
        JOIN identifier_types it ON i.identifier_type_id = it.identifier_type_id
        JOIN pubs p4 ON i.pub_id = p4.pub_id
        WHERE pc4.title_id = titles.title_id
        AND it.identifier_type_name = 'Open Library'
        AND p4.pub_year IS NOT NULL
        AND YEAR(p4.pub_year) > 0
        ORDER BY p4.pub_year ASC
        LIMIT 1) AS openlibrary_id
FROM titles
JOIN canonical_author ON titles.title_id = canonical_author.title_id
JOIN authors ON canonical_author.author_id = authors.author_id
JOIN pub_content ON titles.title_id = pub_content.title_id
JOIN pubs ON pub_content.pub_id = pubs.pub_id
JOIN languages ON titles.title_language = languages.lang_id
JOIN publishers ON pubs.publisher_id = publishers.publisher_id
LEFT JOIN notes ON titles.title_synopsis = notes.note_id
LEFT JOIN (
    SELECT tag_mapping.title_id,
           GROUP_CONCAT(DISTINCT tags.tag_name SEPARATOR ', ') AS tags
    FROM tag_mapping
    JOIN tags ON tag_mapping.tag_id = tags.tag_id
    GROUP BY tag_mapping.title_id
) title_tags ON titles.title_id = title_tags.title_id
WHERE titles.title_ttype = 'NOVEL' -- remove short stories, etc. 
AND pubs.pub_year IS NOT NULL -- remove books that don't have a valid publication year
AND YEAR(pubs.pub_year) > 0
AND languages.lang_name = 'English' -- avoid translations etc
AND titles.title_parent = 0 -- only take the primary title (eliminate when same book is published under separate titles: e.g. "The Hobbit" vs "The Hobbit, or There and Back Again")
AND titles.title_jvn = 'No' -- remove juvenile fiction
GROUP BY titles.title_id, titles.title_title, titles.title_ttype, authors.author_canonical, languages.lang_name, title_tags.tags;
