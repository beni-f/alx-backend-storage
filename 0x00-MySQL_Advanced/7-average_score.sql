-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE num_corrections INT;
    DECLARE avg_score FLOAT;

    SELECT SUM(score), COUNT(*) INTO total_score, num_corrections
    FROM corrections
    WHERE user_id = user_id;

    IF num_corrections > 0 THEN
        SET  avg_score = total_score / num_corrections - 3;
    END IF;

    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END$$

DELIMITER ;