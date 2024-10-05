import {
  Table,
  TableCaption,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  TableFooter,
} from "./table";

export interface Column<T> {
  header: string;
  accessor: (item: T) => React.ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  caption?: string;
  data: T[];
  columns: Column<T>[];
  footer?: React.ReactNode;
  onRowClick?: (item: T) => void;
}

export const DataTable = <T,>({
  caption,
  data,
  columns,
  footer,
  onRowClick,
}: DataTableProps<T>) => {
  return (
    <Table>
      {caption && <TableCaption>{caption}</TableCaption>}
      <TableHeader>
        <TableRow>
          {columns.map((column, index) => (
            <TableHead key={index} className={column.className}>
              {column.header}
            </TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((item, rowIndex) => (
          <TableRow
            key={rowIndex}
            onClick={onRowClick ? () => onRowClick(item) : undefined}
            className={
              onRowClick
                ? "cursor-pointer hover:bg-slate-100 transition-colors"
                : undefined
            }
          >
            {columns.map((column, colIndex) => (
              <TableCell key={colIndex} className={column.className}>
                {column.accessor(item)}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
      {footer && (
        <TableFooter>
          <TableRow>{footer}</TableRow>
        </TableFooter>
      )}
    </Table>
  );
};
