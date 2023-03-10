DELETE_INVOICES = """
    mutation DestroyInvoice($invoiceId: ID!) {
        destroyInvoice(input: { invoiceId: $invoiceId }) {
        invoice {
            id
            }
        errors {
            message
            path
            }
        }
    }
    """
