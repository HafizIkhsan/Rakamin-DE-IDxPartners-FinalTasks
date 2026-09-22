CREATE PROCEDURE DailyTransaction
	@start_date DATE,
	@end_date DATE
AS
BEGIN
	SELECT 
		CAST(TransactionDate AS DATE) as Date,
		COUNT(TransactionId) AS TotalTransactions,
		SUM(Amount) AS TotalAmount
	FROM FactTransaction
	WHERE TransactionDate BETWEEN @start_date AND @end_date
	GROUP BY CAST(TransactionDate AS DATE)
END;
GO