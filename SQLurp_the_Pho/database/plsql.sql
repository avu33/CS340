-- #############################
-- DELETE MenuItem procedure
-- #############################

DROP PROCEDURE IF EXISTS sp_DeleteMenuItem;
DELIMITER //
CREATE PROCEDURE sp_DeleteMenuItem(IN menuItemID INT)
BEGIN
    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on any error
        ROLLBACK;
        -- Propogate the custom error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;
    
        DELETE FROM OrderDetails WHERE menuItemID = menuItemID;
        DELETE FROM MenuItems WHERE menuItemID = menuItemID;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            SET error_message = CONCAT('No matching record found in Menu Items for id, ', menuItemID);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;
    
    COMMIT;

END //
DELIMITER ;


