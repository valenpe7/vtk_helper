import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy

class vtk_helper:

    def __init__(self):
        self.data = None

    def read_vtu(self, filename):
        handle = vtk.vtkXMLUnstructuredGridReader()
        handle.SetFileName(filename)
        handle.Update()
        self.data = handle

    def read_vti(self, filename):
        handle = vtk.vtkXMLImageDataReader()
        handle.SetFileName(filename)
        handle.Update()
        self.data = handle

    def mask_array(self, partition):
        handle = vtk.vtkMaskPoints()
        handle.SetInputConnection(self.data.GetOutputPort())
        handle.SetOnRatio(int(1.0 / partition))
        handle.Update()
        self.data = handle

    def clip_by_scalar(self, array, scalar, invert):
        handle = vtk.vtkClipDataSet()
        handle.SetInputConnection(self.data.GetOutputPort())
        handle.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, array)
        handle.SetValue(scalar)
        if not invert:
            handle.SetInsideOut(True)
        handle.Update()
        self.data = handle

    def transform(self, translate=[0.0, 0.0, 0.0], rotate=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]):
        transformation = vtk.vtkTransform()
        transformation.Translate(translate)
        transformation.RotateX(rotate[0])
        transformation.RotateY(rotate[1])
        transformation.RotateZ(rotate[2])
        transformation.Scale(scale)
        handle = vtk.vtkTransformFilter()
        handle.SetInputConnection(self.data.GetOutputPort())
        handle.SetTransform(transformation)
        handle.Update()
        self.data = handle

    def calculator(self, input_scalar_arrays, output_array, function, attribute_type=0, single=False):
        handle = vtk.vtkArrayCalculator()
        handle.SetInputConnection(self.data.GetOutputPort())
        for input_array in input_scalar_arrays:
            handle.AddScalarArrayName(input_array)
        handle.SetResultArrayName(output_array)
        handle.SetAttributeType(attribute_type)
        if single:
            handle.SetResultArrayType(vtk.VTK_FLOAT)
        handle.SetFunction(function)
        handle.Update()
        self.data = handle

    def pass_arrays(self, point_data_arrays=[], cell_data_arrays=[], field_data_arrays=[]):
        handle = vtk.vtkPassArrays()
        handle.SetInputConnection(self.data.GetOutputPort())
        for array in point_data_arrays:
            handle.AddPointDataArray(array)
        for array in cell_data_arrays:
            handle.AddCellDataArray(array)
        for array in field_data_arrays:
            handle.AddFieldDataArray(array)
        handle.Update()
        self.data = handle

    def get_data_array(self, array_name, attribute_type=0, single=False):
        if attribute_type == 0:
            if self.data.GetOutput().GetPointData().GetArray(array_name) == None:
                if single:
                    return np.float32([])
                else:
                    return np.float64([])
            else:
                if single:
                    return np.float32(vtk_to_numpy(self.data.GetOutput().GetPointData().GetArray(array_name)))
                else:
                    return np.float64(vtk_to_numpy(self.data.GetOutput().GetPointData().GetArray(array_name)))
        if attribute_type == 1:
            if self.data.GetOutput().GetCellData().GetArray(array_name) == None:
                if single:
                    return np.float32([])
                else:
                    return np.float64([])
            else:
                if single:
                    return np.float32(vtk_to_numpy(self.data.GetOutput().GetCellData().GetArray(array_name)))
                else:
                    return np.float64(vtk_to_numpy(self.data.GetOutput().GetCellData().GetArray(array_name)))
        if attribute_type == 2:
            if self.data.GetOutput().GetFieldData().GetArray(array_name) == None:
                if single:
                    return np.float32([])
                else:
                    return np.float64([])
            else:
                if single:
                    return np.float32(vtk_to_numpy(self.data.GetOutput().GetFieldData().GetArray(array_name)))
                else:
                    return np.float64(vtk_to_numpy(self.data.GetOutput().GetFieldData().GetArray(array_name)))

    def get_coordinates(self, single=False):
        if self.data.GetOutput().GetPoints() == None:
            if single:
                return np.float32([])
            else:
                return np.float64([])
        else:
            if single:
                return np.float32(vtk_to_numpy(self.data.GetOutput().GetPoints().GetData()))
            else:
                return np.float64(vtk_to_numpy(self.data.GetOutput().GetPoints().GetData()))

    def get_data(self):
        return self.data.GetOutput()
