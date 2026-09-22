CREATE PROCEDURE BalancePerCustomer
	@name VARCHAR(255)
AS
BEGIN
	SELECT 
		c.CustomerName, 
		a.AccountType, 
		a.Balance, 
		SUM(CASE
			WHEN f.TransactionType = 'Deposit' THEN (1 * f.amount)
			ELSE ((-1) * f.amount)
		END) + a.Balance AS CurrentBalance
	FROM FactTransaction f
	INNER JOIN DimAccount a
	ON f.AccountId = a.AccountId
	INNER JOIN DimCustomer c
	ON a.CustomerId = c.CustomerId
	WHERE c.CustomerName LIKE '%' + @name + '%'
		AND a.status = 'active'
	GROUP BY c.CustomerName, a.AccountType, a.Balance
END;