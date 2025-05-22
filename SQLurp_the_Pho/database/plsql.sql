-- #############################
-- DELETE MenuItem procedure
-- #############################

DROP PROCEDURE IF EXISTS sp_DeleteMenuItem;
DELIMITER //

CREATE PROCEDURE sp_DeleteMenuItem(IN p_menuItemID INT)
BEGIN
    DECLARE error_message VARCHAR(255); 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

        DELETE FROM MenuItems WHERE menuItemID = p_menuItemID;

        IF ROW_COUNT() = 0 THEN
            SET error_message = CONCAT('No matching record found in MenuItems for ID ', p_menuItemID);
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;
END //

DELIMITER ;


