-- all categories.

USE BioMrcDB;

INSERT INTO
    categories (
        id,
        created_at,
        updated_at,
        name,
        `desc`
    )
VALUES (
        1,
        NOW(),
        NOW(),
        "Moroccan Oils",
        " Moroccan oils are renowned for their exceptional quality and diverse benefits, derived from the rich agricultural heritage of Morocco. These oils are extracted from locally grown plants and nuts, utilizing traditional methods that preserve their natural properties. Moroccan oils are celebrated for their versatility, offering both culinary delights and cosmetic benefits."
    );
